#!/usr/bin/env bash
# Upgrades Kordalo to a released version. Sites are briefly unavailable during migration,
# so announce a maintenance window. Also run automatically by the Release workflow.
# Usage: bash scripts/upgrade.sh v1.2.0
source "$(dirname "$0")/lib.sh"
load_env
NEW="${1:?usage: upgrade.sh <release tag, e.g. v1.2.0>}"
OLD="$KORDALO_VERSION"

echo "==> Safety backup before upgrading $OLD -> $NEW"
if [ -n "${RESTIC_REPOSITORY:-}" ]; then bash scripts/backup.sh
else for s in $(list_sites); do bench --site "$s" backup; done; fi

set_env KORDALO_VERSION "$NEW"
if ! docker compose pull; then
  set_env KORDALO_VERSION "$OLD"; echo "Image $NEW not found; nothing changed." >&2; exit 1
fi
docker compose up -d

for s in $(list_sites); do
  echo "==> Migrating $s"
  bench --site "$s" migrate
done
docker compose restart
echo "Upgraded to $NEW. Rollback (if needed): restore the pre-upgrade backup with $OLD."
