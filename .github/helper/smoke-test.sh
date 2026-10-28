#!/bin/bash
# Boots a built Kordalo image with the production compose file, creates a site,
# and checks it actually works and is fully rebranded.
# Usage: smoke-test.sh <image-name> <tag>      (run from the repo root)
set -euo pipefail
IMAGE="${1:?image}"; TAG="${2:?tag}"
SITE=smoke.localhost
cd deploy

cat > .env <<EOF
KORDALO_IMAGE=$IMAGE
KORDALO_VERSION=$TAG
PRIMARY_DOMAIN=$SITE
SITE_DOMAINS="$SITE"
ACME_EMAIL=ci@example.com
DB_ROOT_PASSWORD=ci-root-password
ADMIN_PASSWORD=ci-admin-password
EOF

cleanup() {
  if [ "${1:-0}" != 0 ]; then docker compose logs --tail 80 backend frontend || true; fi
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
  rm -f .env
}
trap 'cleanup $?' EXIT

# Everything except Caddy (no real domain / certificates in CI).
docker compose up -d --quiet-pull $(docker compose config --services | grep -vx caddy)
docker compose exec -T backend wait-for-it -t 180 db:3306
docker compose exec -T backend bench new-site "$SITE" \
  --mariadb-user-host-login-scope='%' --admin-password ci-admin-password \
  --db-root-username root --db-root-password ci-root-password --install-app kordalo

fetch() { docker run --rm --network kordalo_default curlimages/curl:8.10.1 -fsS -H "Host: $SITE" "$@"; }
fail() { echo "SMOKE TEST FAILED: $*" >&2; exit 1; }

echo "--> ping";      fetch http://frontend:8080/api/method/ping | grep -q pong || fail "ping"
echo "--> login page"; login=$(fetch http://frontend:8080/login)
grep -q "Kordalo" <<<"$login" || fail "login page does not mention Kordalo"
if grep -qi "erpnext" <<<"$login"; then fail "login page still mentions the old name"; fi
echo "--> logo";      fetch -o /dev/null http://frontend:8080/assets/kordalo/images/kordalo-logo.svg || fail "logo asset missing"
echo "--> apps";      docker compose exec -T backend bench --site "$SITE" list-apps | grep -q kordalo || fail "kordalo not installed"
echo "--> login API"
fetch -X POST -H "Content-Type: application/json" \
  -d '{"usr":"Administrator","pwd":"ci-admin-password"}' http://frontend:8080/api/method/login | grep -q "Logged In" || fail "login"
echo "--> setup wizard registered for kordalo (patch_frappe.py)"
docker compose exec -T backend bench --site "$SITE" execute frappe.db.get_value \
  --args '["Installed Application", {"app_name": "kordalo"}, "has_setup_wizard"]' | grep -qx 1 || fail "kordalo has no setup wizard"

echo "Smoke test passed."
