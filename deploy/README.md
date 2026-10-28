# Running Kordalo on Hetzner

One 4 GB Hetzner server running the Kordalo Docker image, with automatic HTTPS, a hardened firewall,
nightly encrypted off-site backups, and one-command scripts to restore, upgrade and add customers.

**Cost:** about €5–8/month (server + Hetzner backups + a few cents of Backblaze storage) + ~$10/year domain.
**Realistic availability:** ~99.5% excluding announced upgrade windows.

> Use **personal** accounts and email for everything below, not work accounts.

## One-time setup (≈ 45 minutes)

### 1. Accounts you create yourself
| What | Where | Cost |
|---|---|---|
| Domain `kordalo.com` | Cloudflare Registrar or Porkbun | ~$10/year |
| Hetzner Cloud | https://accounts.hetzner.com/signUp (needs ID check + card) | pay-as-you-go |
| Backblaze B2 (off-site backups) | https://www.backblaze.com/sign-up/cloud-storage | first 10 GB free |
| UptimeRobot (downtime alerts) | https://uptimerobot.com | free |
| Healthchecks.io (backup alerts) | https://healthchecks.io | free |

### 2. Prepare on your PC (PowerShell, in this `deploy` folder)
```powershell
.\scripts\setup-local.ps1
```
Creates an SSH key and copies the server config to your clipboard.

### 3. Create the server (Hetzner Cloud Console → Add Server)
- **Location:** closest to your customers
- **Image:** Ubuntu 24.04 · **Type:** Shared vCPU → x86 → **CX23** (2 vCPU / 4 GB)
- **Networking:** IPv4 + IPv6 · **Cloud config:** paste your clipboard · **Backups:** ✅ enable
- **Name:** `kordalo-prod-1`. Copy its **IPv4 address**; wait ~3 minutes for setup to finish.

### 4. DNS
Add an **A record** `app` → server IPv4 (and **AAAA** → IPv6). On Cloudflare: **DNS only** (grey cloud).
Optional: a wildcard `*` record too, so every `<customer>.kordalo.com` works without more DNS changes.

### 5. Backup bucket (Backblaze B2)
Create a **private** bucket and an **Application Key** restricted to it. Note the endpoint
(e.g. `s3.us-west-004.backblazeb2.com`), keyID and applicationKey.

### 6. Fill in `.env`
```powershell
Copy-Item .env.example .env
code .env
```
Set `ACME_EMAIL`, `RESTIC_REPOSITORY=s3:https://<endpoint>/<bucket>`, `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `KORDALO_VERSION` (latest tag from the GitHub Releases page).
Leave the password fields empty; they get generated.

### 7. Upload and install
```powershell
.\scripts\push.ps1 -ServerIp <your-server-ip>
ssh kordalo
bash ~/kordalo-deploy/scripts/deploy.sh
```
Save the printed passwords in a password manager. `RESTIC_PASSWORD` is the only way to decrypt backups.
Open `https://app.kordalo.com`, log in as `Administrator`, and complete the setup wizard.

### 8. Monitoring
- **UptimeRobot:** monitor `https://app.kordalo.com/api/method/ping` every 5 min.
- **Healthchecks.io:** check with period 1 day / grace 2 h; put its URL in `HEALTHCHECK_URL` in the server's `.env`.

### 9. Prove your backups work
Run `bash ~/kordalo-deploy/scripts/backup.sh`, then on a throwaway CX23 server do steps 3, 6, 7 but run
`scripts/restore.sh` instead of `deploy.sh`. Check your data, delete the test server.

## Day-to-day (`ssh kordalo`, then `cd ~/kordalo-deploy`)

| Task | Command |
|---|---|
| New customer | point DNS first, then `bash scripts/add-site.sh acme.kordalo.com` |
| Upgrade (or let the Release workflow do it) | `bash scripts/upgrade.sh v1.2.0` |
| Manual backup | `bash scripts/backup.sh` |
| Status / logs | `docker compose ps` · `docker compose logs -f --tail 100 backend` |
| Restart everything | `docker compose restart` |
| Disaster recovery to a new server | `bash scripts/restore.sh` |

## What protects your uptime
- Every container auto-restarts; the stack comes back after a reboot.
- 4 GB swap + tuned MariaDB memory; Docker logs capped so the disk can't fill.
- Automatic security updates, firewall (SSH/HTTP/HTTPS only), key-only SSH, fail2ban.
- Two backup layers: Hetzner daily snapshots + encrypted nightly restic backups at Backblaze.
- Every release is smoke-tested in CI before it can reach the server.

## When to grow
- RAM regularly > 80% (`free -h`) → resize to CX33/CX43 in the Hetzner console (~2 min downtime).
- Customers need a contractual SLA above 99.5% → multi-server setup with a managed database.
