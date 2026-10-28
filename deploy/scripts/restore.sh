#!/usr/bin/env bash
# Disaster recovery onto a FRESH server: restores all sites from the latest off-site backup.
# Prereq: cloud-init done, this folder copied over, .env filled with the SAME RESTIC_* values.
# Usage: bash scripts/restore.sh [snapshot-id]   (default: latest)
source "$(dirname "$0")/lib.sh"
load_env
SNAPSHOT="${1:-latest}"
[ -z "${DB_ROOT_PASSWORD:-}" ] && set_env DB_ROOT_PASSWORD "$(gen_secret 32)"

if docker volume inspect kordalo_sites >/dev/null 2>&1; then
  read -rp "Existing Kordalo data found on this server. Overwrite it? (type YES) " ok
  [ "$ok" = "YES" ] || exit 1
  docker compose down
fi

echo "==> Restoring files from snapshot $SNAPSHOT"
docker volume create kordalo_sites >/dev/null
restic_run -v kordalo_sites:/data/sites "$RESTIC_IMAGE" \
  restore "$SNAPSHOT" --target / --include /data/sites
restic_run "$RESTIC_IMAGE" \
  dump "$SNAPSHOT" /data/env/.env > .env.from-backup || true

echo "==> Starting the stack"
docker compose pull
docker compose up -d
docker compose exec -T backend wait-for-it -t 180 db:3306

for site in $(list_sites); do
  sql=$(docker compose exec -T backend bash -c \
    "ls -t sites/$site/private/backups/*-database.sql.gz 2>/dev/null | head -1")
  [ -n "$sql" ] || { echo "!! No database dump for $site, skipping"; continue; }
  echo "==> Restoring $site from $sql"
  bench --site "$site" --force restore "/home/frappe/frappe-bench/$sql" \
    --db-root-username root --db-root-password "$DB_ROOT_PASSWORD"
  bench --site "$site" migrate
done

docker compose restart
echo "Restore complete. The old .env is saved as .env.from-backup for reference."
echo "Point DNS at this server, then run: bash scripts/deploy.sh  (re-installs the backup cron)."
