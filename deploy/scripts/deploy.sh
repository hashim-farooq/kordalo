#!/usr/bin/env bash
# First-time install (safe to re-run): generates secrets, starts the stack,
# creates the primary site, and installs the nightly backup cron job.
source "$(dirname "$0")/lib.sh"
load_env

for v in PRIMARY_DOMAIN SITE_DOMAINS ACME_EMAIL KORDALO_VERSION; do
  [ -n "${!v:-}" ] && [[ "${!v}" != *example.com* ]] || { echo "Set $v in .env first." >&2; exit 1; }
done

NEW_SECRETS=0
for v in DB_ROOT_PASSWORD ADMIN_PASSWORD RESTIC_PASSWORD; do
  if [ -z "${!v:-}" ]; then set_env "$v" "$(gen_secret 32)"; NEW_SECRETS=1; fi
done

echo "==> Pulling images and starting the stack"
docker compose pull
docker compose up -d
docker compose exec -T backend wait-for-it -t 180 db:3306
docker compose exec -T backend wait-for-it -t 60 redis-cache:6379
docker compose exec -T backend wait-for-it -t 60 redis-queue:6379

if list_sites | grep -qx "$PRIMARY_DOMAIN"; then
  echo "==> Site $PRIMARY_DOMAIN already exists"
else
  echo "==> Creating site $PRIMARY_DOMAIN (takes a few minutes)"
  bench new-site "$PRIMARY_DOMAIN" \
    --mariadb-user-host-login-scope='%' \
    --admin-password "$ADMIN_PASSWORD" \
    --db-root-username root --db-root-password "$DB_ROOT_PASSWORD" \
    --install-app kordalo
  bench --site "$PRIMARY_DOMAIN" set-config host_name "https://$PRIMARY_DOMAIN"
  bench --site "$PRIMARY_DOMAIN" enable-scheduler
fi

if [ -n "${RESTIC_REPOSITORY:-}" ]; then
  echo "==> Preparing off-site backup repository"
  restic_run "$RESTIC_IMAGE" cat config >/dev/null 2>&1 || restic_run "$RESTIC_IMAGE" init
  echo "30 2 * * * $(whoami) bash $DEPLOY_DIR/scripts/backup.sh >> $HOME/kordalo-backup.log 2>&1" \
    | sudo tee /etc/cron.d/kordalo-backup >/dev/null
  echo "    Nightly backup scheduled for 02:30 UTC."
else
  echo "!!  RESTIC_REPOSITORY is empty - NO off-site backups are configured yet."
fi

echo
echo "Done. Open https://$PRIMARY_DOMAIN  (user: Administrator)"
if [ "$NEW_SECRETS" = 1 ]; then
  echo
  echo "New secrets were generated and saved in $DEPLOY_DIR/.env."
  echo "Copy these into your password manager NOW:"
  grep -E '^(DB_ROOT_PASSWORD|ADMIN_PASSWORD|RESTIC_PASSWORD)=' .env
fi
