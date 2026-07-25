#!/usr/bin/env bash
set -euo pipefail

DATABASE="${1:-Autonomo}"
BACKUP_ROOT="${BACKUP_ROOT:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$DATABASE-$STAMP"

mkdir -p "$BACKUP_DIR"

docker compose exec -T db pg_dump -U odoo -d "$DATABASE" > "$BACKUP_DIR/$DATABASE.sql"
docker compose cp "odoo:/var/lib/odoo/filestore/$DATABASE" "$BACKUP_DIR/filestore"
cp -R config "$BACKUP_DIR/config"

{
  echo "database=$DATABASE"
  echo "created_at=$(date -Iseconds)"
  echo "git_commit=$(git rev-parse HEAD)"
  echo "docker_version=$(docker version --format '{{.Server.Version}}')"
  echo "compose_version=$(docker compose version)"
  echo "note=El volumen Docker no es copia de seguridad. Este backup incluye pg_dump, filestore, config, commit y hashes."
} > "$BACKUP_DIR/metadata.txt"

(cd "$BACKUP_DIR" && find . -type f ! -name SHA256SUMS.txt -print0 | xargs -0 sha256sum > SHA256SUMS.txt)
find "$BACKUP_ROOT" -maxdepth 1 -type d -name "$DATABASE-*" -mtime "+$RETENTION_DAYS" -exec rm -rf {} +

echo "Backup creado en $BACKUP_DIR"
