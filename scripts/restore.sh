#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${1:?Uso: scripts/restore.sh RUTA_BACKUP [DATABASE]}"
DATABASE="${2:-Autonomo}"
SQL_FILE="$BACKUP_DIR/$DATABASE.sql"
FILESTORE_DIR="$BACKUP_DIR/filestore"

test -f "$SQL_FILE" || { echo "No existe $SQL_FILE" >&2; exit 1; }

echo "Restaurando $DATABASE desde $BACKUP_DIR"
if [ -d "$FILESTORE_DIR" ]; then
  docker compose exec -T odoo sh -lc "rm -rf /var/lib/odoo/filestore/$DATABASE"
fi
docker compose stop odoo
docker compose exec -T db dropdb -U odoo --if-exists "$DATABASE"
docker compose exec -T db createdb -U odoo "$DATABASE"
docker compose exec -T db psql -U odoo -d "$DATABASE" < "$SQL_FILE"

if [ -d "$FILESTORE_DIR" ]; then
  docker compose cp "$FILESTORE_DIR" "odoo:/var/lib/odoo/filestore/$DATABASE"
fi

docker compose up -d
echo "Restauración terminada. Revisa Odoo y ejecuta pruebas funcionales."
