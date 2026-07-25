param(
    [Parameter(Mandatory = $true)][string]$BackupDir,
    [string]$Database = "Autonomo"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $BackupDir)) { throw "No existe $BackupDir" }

$sqlFile = Join-Path $BackupDir "$Database.sql"
$filestoreDir = Join-Path $BackupDir "filestore"
if (-not (Test-Path $sqlFile)) { throw "No existe $sqlFile" }

Write-Host "Restaurando $Database desde $BackupDir"
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
