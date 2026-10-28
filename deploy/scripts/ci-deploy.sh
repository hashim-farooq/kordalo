#!/usr/bin/env bash
# Entry point for the Release workflow (runs on the server over SSH).
# Merges the settings CI sent in .env.ci into .env, then installs on the first run
# or upgrades on later runs.
# Usage: bash scripts/ci-deploy.sh <release tag>
source "$(dirname "$0")/lib.sh"
VERSION="${1:?usage: ci-deploy.sh <release tag>}"

FIRST_RUN=0
if [ ! -f .env ]; then cp .env.example .env; FIRST_RUN=1; fi
if [ -f .env.ci ]; then
  while IFS='=' read -r key value; do
    [ -n "$key" ] && [ -n "$value" ] && set_env "$key" "$value"
  done < .env.ci
  rm -f .env.ci
fi
load_env
[ "$FIRST_RUN" = 1 ] && set_env SITE_DOMAINS "\"$PRIMARY_DOMAIN\"" && load_env

if [ -n "$(docker compose ps -q backend 2>/dev/null)" ]; then
  bash scripts/upgrade.sh "$VERSION"
else
  set_env KORDALO_VERSION "$VERSION"
  bash scripts/deploy.sh
fi
