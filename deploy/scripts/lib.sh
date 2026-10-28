# Shared helpers. Sourced by the other scripts; run from the deploy directory.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
DEPLOY_DIR="$(pwd)"

RESTIC_IMAGE=restic/restic:0.17.3

load_env() {
  [ -f .env ] || { echo "Missing .env - run: cp .env.example .env  and fill it in." >&2; exit 1; }
  sed -i 's/\r$//' .env   # tolerate Windows line endings
  chmod 600 .env
  set -a; source .env; set +a
}

# Writes KEY=VALUE into .env, replacing any existing line for KEY.
set_env() {
  if grep -q "^$1=" .env; then sed -i "s|^$1=.*|$1=$2|" .env; else echo "$1=$2" >> .env; fi
  export "$1=$2"
}

gen_secret() { tr -dc 'A-Za-z0-9' </dev/urandom | head -c "${1:-32}"; }

bench() { docker compose exec -T backend bench "$@"; }

list_sites() {
  docker compose exec -T backend bash -c \
    'for d in sites/*/; do [ -f "$d/site_config.json" ] && basename "$d"; done; true'
}

restic_run() {
  docker run --rm -i --hostname kordalo \
    -e RESTIC_REPOSITORY -e RESTIC_PASSWORD -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY \
    "$@"
}

ping_healthcheck() {
  [ -n "${HEALTHCHECK_URL:-}" ] && curl -fsS -m 10 --retry 3 "${HEALTHCHECK_URL}$1" >/dev/null || true
}
