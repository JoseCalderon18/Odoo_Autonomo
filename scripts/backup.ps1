param(
    [string]$Database = "Autonomo",
    [string]$BackupRoot = ".\backups",
    [int]$RetentionDays = 30,
    [string]$ExternalDriveLabel = ""
)

$ErrorActionPreference = "Stop"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$targetRoot = $BackupRoot

if ($ExternalDriveLabel) {
    $drive = Get-Volume | Where-Object { $_.FileSystemLabel -eq $ExternalDriveLabel } | Select-Object -First 1
    if ($drive -and $drive.DriveLetter) {
        $targetRoot = "$($drive.DriveLetter):\odoo19-backups"
    }
}

$backupDir = Join-Path $targetRoot "$Database-$stamp"
New-Item -ItemType Directory -Force $backupDir | Out-Null

$dbFile = Join-Path $backupDir "$Database.sql"
$containerDbFile = "/tmp/$Database.sql"
$metaFile = Join-Path $backupDir "metadata.txt"
$hashFile = Join-Path $backupDir "SHA256SUMS.txt"
$filestoreDir = Join-Path $backupDir "filestore"
$configDir = Join-Path $backupDir "config"

docker compose up -d db
docker compose exec -T db pg_isready -U odoo -d postgres | Out-Null
docker compose exec -T db psql -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$Database'" | Select-String "1" | Out-Null
docker compose exec -T db pg_dump -U odoo -d $Database -f $containerDbFile
docker compose cp "db:$containerDbFile" $dbFile

if (-not (Test-Path $dbFile)) {
    throw "No se ha creado $dbFile"
}

$dbFileSize = (Get-Item $dbFile).Length
if ($dbFileSize -le 1024) {
    throw "Backup SQL invalido: $dbFile pesa $dbFileSize bytes. No se considera copia valida."
}

docker compose cp "odoo:/var/lib/odoo/filestore/$Database" $filestoreDir
Copy-Item -Recurse -Force ".\config" $configDir

$gitCommit = git rev-parse HEAD
$dockerVersion = docker version --format '{{.Server.Version}}'
$composeVersion = docker compose version
@"
database=$Database
created_at=$(Get-Date -Format o)
git_commit=$gitCommit
docker_version=$dockerVersion
compose_version=$composeVersion
odoo_container=odoo
db_container=db
note=El volumen Docker no es copia de seguridad. Este backup incluye pg_dump, filestore, config, commit y hashes.
sql_size_bytes=$dbFileSize
"@ | Set-Content -Path $metaFile -Encoding utf8

Get-ChildItem -Path $backupDir -Recurse -File | ForEach-Object {
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName
    "$($hash.Hash)  $($_.FullName.Substring($backupDir.Length + 1))"
} | Set-Content -Path $hashFile -Encoding utf8

Get-ChildItem -Path $targetRoot -Directory -Filter "$Database-*" |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$RetentionDays) } |
    Remove-Item -Recurse -Force

Write-Host "Backup creado en $backupDir"
