#!/usr/bin/env bash
# Dumps every site's database, then pushes the whole sites volume (DB dumps, uploaded
# files, site configs incl. encryption keys) plus .env to the encrypted off-site restic repo.
source "$(dirname "$0")/lib.sh"
load_env
[ -n "${RESTIC_REPOSITORY:-}" ] || { echo "RESTIC_REPOSITORY not set" >&2; exit 1; }

ping_healthcheck /start
trap 'ping_healthcheck /fail' ERR

echo "$(date -u +%FT%TZ) backup starting"
for site in $(list_sites); do
  bench --site "$site" backup --compress
done

restic_run -v kordalo_sites:/data/sites:ro -v "$DEPLOY_DIR/.env:/data/env/.env:ro" \
  "$RESTIC_IMAGE" backup /data --exclude '/data/sites/*/locks'

restic_run "$RESTIC_IMAGE" forget --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune

# Keep only 3 days of dumps on the server itself; older ones live off-site.
docker compose exec -T backend find sites -path '*/private/backups/*' -type f -mtime +3 -delete

echo "$(date -u +%FT%TZ) backup finished"
ping_healthcheck ""
