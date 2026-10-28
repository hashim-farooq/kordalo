#!/usr/bin/env bash
# Adds a new customer: a separate Kordalo site (own database) on its own domain.
# Usage: bash scripts/add-site.sh acme.kordalo.com
# Point the domain's DNS A record at this server BEFORE running.
source "$(dirname "$0")/lib.sh"
load_env
DOMAIN="${1:?usage: add-site.sh <domain>}"

if list_sites | grep -qx "$DOMAIN"; then echo "$DOMAIN already exists" >&2; exit 1; fi

PASS="$(gen_secret 20)"
bench new-site "$DOMAIN" \
  --mariadb-user-host-login-scope='%' \
  --admin-password "$PASS" \
  --db-root-username root --db-root-password "$DB_ROOT_PASSWORD" \
  --install-app kordalo
bench --site "$DOMAIN" set-config host_name "https://$DOMAIN"
bench --site "$DOMAIN" enable-scheduler

set_env SITE_DOMAINS "\"$SITE_DOMAINS $DOMAIN\""
load_env
docker compose up -d caddy   # picks up the new domain and fetches its certificate

echo "Created https://$DOMAIN  Administrator password: $PASS  (save it now)"
