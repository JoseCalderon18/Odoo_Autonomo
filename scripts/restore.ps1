param(
    [string]$BackupDir = "",
    [string]$Database = "Autonomo"
)

$ErrorActionPreference = "Stop"
if (-not $BackupDir) {
    $latest = Get-ChildItem -Path ".\backups" -Directory -Filter "$Database-*" |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if (-not $latest) {
        throw "No se ha indicado -BackupDir y no se encontro ningun backup en .\backups\$Database-*"
    }
    $BackupDir = $latest.FullName
}

if (-not (Test-Path $BackupDir)) { throw "No existe $BackupDir" }

$sqlFile = Join-Path $BackupDir "$Database.sql"
$filestoreDir = Join-Path $BackupDir "filestore"
if (-not (Test-Path $sqlFile)) { throw "No existe $sqlFile" }

$sqlFileSize = (Get-Item $sqlFile).Length
if ($sqlFileSize -le 1024) {
    throw "El backup SQL existe pero no es valido: $sqlFile pesa $sqlFileSize bytes. Necesitas un backup nuevo."
}

Write-Host "Restaurando $Database desde $BackupDir"
docker compose up -d db
docker compose up -d odoo
if (Test-Path $filestoreDir) {
    docker compose exec -T odoo sh -lc "rm -rf /var/lib/odoo/filestore/$Database"
}
docker compose stop odoo
docker compose exec -T db dropdb -U odoo --if-exists $Database
docker compose exec -T db createdb -U odoo $Database
Get-Content -Raw $sqlFile | docker compose exec -T db psql -U odoo -d $Database

if (Test-Path $filestoreDir) {
    docker compose cp $filestoreDir "odoo:/var/lib/odoo/filestore/$Database"
}

docker compose up -d
Write-Host "Restauración terminada. Revisa Odoo y ejecuta pruebas funcionales."
