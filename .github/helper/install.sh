#!/bin/bash
# Builds a bench with Kordalo on a GitHub-hosted runner and creates `test_site`.
# Mirrors the upstream engine's CI (Python 3.14, Node 24, MariaDB 11.8), adapted
# for the renamed app: Frappe gets patch_frappe.py, and the `payments` app
# (which upstream tests install alongside) is renamed in place to import kordalo.
set -euo pipefail

source "$GITHUB_WORKSPACE/tools/rebrand/upstream.env"
REBRAND="$GITHUB_WORKSPACE/tools/rebrand"
DB_ROOT=(--host 127.0.0.1 --port 3306 -u root -proot)

group() { echo "::group::$1"; }
endgroup() { echo "::endgroup::"; }

group "System packages"
sudo apt-get update -qq
sudo apt-get install -y -qq --no-install-recommends redis-server libcups2-dev mariadb-client libmariadb-dev pkg-config
wget -q -O /tmp/wkhtmltox.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt-get install -y -qq /tmp/wkhtmltox.deb
pip install -q frappe-bench
endgroup

group "Bench init (frappe $FRAPPE_TAG)"
cd ~
bench init --skip-assets --frappe-branch "$FRAPPE_TAG" --python "$(which python)" frappe-bench
cd ~/frappe-bench
python "$REBRAND/patch_frappe.py" apps/frappe
sed -i 's/^watch:/# watch:/; s/^schedule:/# schedule:/; s/^socketio:/# socketio:/; s/^redis_socketio:/# redis_socketio:/' Procfile
CI=Yes bench build --app frappe
endgroup

group "Database"
for _ in $(seq 1 60); do mariadb-admin ping "${DB_ROOT[@]}" --silent && break; sleep 1; done
mariadb "${DB_ROOT[@]}" -e "SET GLOBAL character_set_server = 'utf8mb4'; SET GLOBAL collation_server = 'utf8mb4_unicode_ci';"
mariadb "${DB_ROOT[@]}" -e "SET GLOBAL innodb_flush_log_at_trx_commit=0; SET GLOBAL sync_binlog=0;"
mariadb "${DB_ROOT[@]}" -e "CREATE USER 'test_frappe'@'%' IDENTIFIED BY 'test_frappe'; CREATE DATABASE test_frappe; GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'%'; FLUSH PRIVILEGES;"
mkdir -p sites/test_site
cp "$GITHUB_WORKSPACE/.github/helper/site_config.json" sites/test_site/site_config.json
endgroup

group "Apps"
bench get-app payments --branch "$PAYMENTS_REF"
python "$REBRAND/rebrand.py" inplace apps/payments
bench get-app kordalo "$GITHUB_WORKSPACE"
bench setup requirements --dev
endgroup

group "Start bench and reinstall test_site"
bench start >> ~/frappe-bench/bench_start.log 2>&1 &
for port in $(python -c "import json,re;c=json.load(open('sites/common_site_config.json'));print(' '.join(re.search(r':(\d+)',c[k]).group(1) for k in ('redis_cache','redis_queue')))"); do
  for _ in $(seq 1 120); do (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null && break; sleep 1; done
done
bench --site test_site reinstall --yes
endgroup
