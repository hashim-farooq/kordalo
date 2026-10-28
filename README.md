<div align="center">
  <img src="tools/rebrand/branding/wordmark.svg" height="64" alt="Kordalo">
  <p><b>Business management for growing companies</b>: accounting, inventory, sales, purchasing,
  manufacturing, projects and more, in one place.</p>
</div>

## Repository layout

| Path | What it is |
|---|---|
| `kordalo/`, `banking/`, `pyproject.toml`, … | The Kordalo app (a Frappe app). **Generated** from the upstream engine by `tools/rebrand`. |
| `tools/rebrand/` | `rebrand.py` (regenerates the app from upstream), `check.py` (guards against leftover old names), `patch_frappe.py` (framework compatibility patch), logos, and `upstream.env` (pinned upstream versions). |
| `docker/` | Production image (`docker build -f docker/Containerfile .`). |
| `deploy/` | Everything to run Kordalo on a Hetzner server. Start with [deploy/README.md](deploy/README.md). |
| `.github/` | CI/CD. |

## CI/CD

| Workflow | Trigger | What it does |
|---|---|---|
| **CI** | every PR and push to `main` | Lint (pre-commit: ruff, eslint, prettier, JSON/YAML checks) · rebrand guard · JS unit tests · full server test suite on MariaDB (4 parallel shards) · Docker build + live smoke test (boots the image, creates a site, checks login, branding and setup wizard). On `main`, publishes `ghcr.io/hashim-farooq/kordalo:main`. |
| **Release** | push a tag `v*` on `main` | Builds, smoke-tests and publishes `ghcr.io/hashim-farooq/kordalo:<tag>` + `:latest`, creates a GitHub Release, then (once enabled) deploys to production after manual approval and verifies health. |
| **Upstream sync** | weekly + manual | If a newer upstream v16 release exists, regenerates the app and opens a PR for CI to test. |

`main` is protected: changes land through pull requests with all CI checks green.

### Releasing
```bash
git checkout main && git pull
git tag v1.1.0 && git push origin v1.1.0
```

### Enabling automatic deploys (after the server exists)
1. Create a deploy key: `ssh-keygen -t ed25519 -f kordalo_deploy -N ""`, and append `kordalo_deploy.pub` to
   `~/.ssh/authorized_keys` on the server.
2. Repo **Settings → Secrets and variables → Actions**:
   secrets `DEPLOY_HOST` (server IP), `DEPLOY_SSH_KEY` (contents of `kordalo_deploy`),
   `DEPLOY_KNOWN_HOSTS` (output of `ssh-keyscan <server-ip>`);
   variables `PRODUCTION_URL=https://app.kordalo.com` and `DEPLOY_ENABLED=true`.
3. The `production` environment requires your approval before each deploy.

## Developing locally
Use a standard Frappe bench (Python 3.14, Node 24, MariaDB 11.8):
```bash
bench init --frappe-branch v16.53.0 kordalo-bench && cd kordalo-bench
python /path/to/kordalo/tools/rebrand/patch_frappe.py apps/frappe
bench get-app kordalo /path/to/kordalo
bench new-site dev.localhost --install-app kordalo
```

**Don't hand-edit generated app code** for durable changes: the next upstream sync regenerates it.
Put customisations in `tools/rebrand/` (if it's about naming/branding) or in a separate Frappe app.

## License
GNU GPL v3; see [license.txt](license.txt) and [NOTICE.md](NOTICE.md).
