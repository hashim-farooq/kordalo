# Deploying Kordalo (CI/CD)

Production is one Hetzner server running the Kordalo Docker image. **Deployments are done by GitHub
Actions**: each release (a `v*` tag on `main`) is built, smoke-tested and published, and then, after you
approve it, deployed to the server. The pipeline uploads this folder, writes the server's `.env` from
GitHub Secrets, installs Kordalo on the first run or backs up and upgrades on later runs, and then checks
that the site is healthy.

```
PR ──► CI (lint · rebrand guard · JS tests · full server tests · Docker smoke test)
        │ merge
main ──► CI ──► image ghcr.io/hashim-farooq/kordalo:main
        │ git tag v1.2.0
tag ──► Release: build ► smoke test ► publish :v1.2.0 ► GitHub Release
                      ► [you approve] ► deploy to server ► health check https://app.kordalo.com
```

**Cost:** about €5–8/month (Hetzner CX23 + backups, a few cents of Backblaze) + ~$10/year domain.
**Realistic availability:** ~99.5% excluding announced upgrade windows.

---

## One-time setup

> Use **personal** accounts and email only, never work accounts.

### Already prepared
- SSH keys in `~/.ssh`: `kordalo_hetzner` (your own emergency access) and `kordalo_ci_deploy`
  (used by GitHub Actions; its public half is `deploy/ci-deploy.pub`).
- `deploy/cloud-init.generated.yaml`: server setup with both public keys filled in (git-ignored).
  Re-create it any time with `.\scripts\setup-local.ps1`.
- `KORDALO-SECRETS.txt` (next to the repo folder): freshly generated passwords, ready to paste into GitHub.
- The `production` environment requires your approval before every deploy.

### Your steps (≈ 40 minutes)
1. **Buy the domain** `kordalo.com` (Cloudflare Registrar or Porkbun).
2. **Create a Hetzner Cloud account** at https://accounts.hetzner.com/signUp (ID check + card).
3. **Create the server:** Cloud Console → *Add Server*:
   Ubuntu 24.04 · Shared vCPU x86 **CX23** · location near your customers · IPv4 + IPv6 ·
   **Backups on** · name `kordalo-prod-1` · *Cloud config*: paste the whole of
   `deploy/cloud-init.generated.yaml`. Copy the server's **IPv4** address.
4. **DNS:** at your registrar add `A  app  → <server IPv4>` (and `AAAA app → <IPv6>`).
   On Cloudflare, set the record to **DNS only** (grey cloud). Optionally add a wildcard `*` record for customer subdomains.
5. **Backblaze B2** (https://www.backblaze.com): create a **private** bucket and an Application Key restricted
   to it. Note the endpoint (e.g. `s3.us-west-004.backblazeb2.com`), keyID and applicationKey.
6. **GitHub settings:** go to github.com/hashim-farooq/kordalo → *Settings → Secrets and variables → Actions*.
   - *Secrets* tab → *New repository secret* for each:

     | Name | Value |
     |---|---|
     | `DEPLOY_SSH_KEY` | entire contents of `C:\Users\hashi\.ssh\kordalo_ci_deploy` (incl. BEGIN/END lines) |
     | `DB_ROOT_PASSWORD`, `ADMIN_PASSWORD`, `RESTIC_PASSWORD` | from `KORDALO-SECRETS.txt` |
     | `ACME_EMAIL` | your personal email (certificate expiry notices) |
     | `RESTIC_REPOSITORY` | `s3:https://<endpoint>/<bucket>` |
     | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Backblaze keyID / applicationKey |

   - *Variables* tab → *New repository variable*: `PRIMARY_DOMAIN` = `app.kordalo.com` ·
     `DEPLOY_HOST` = server IPv4 · `DEPLOY_ENABLED` = `true`
   - Save the three passwords in a password manager, then delete `KORDALO-SECRETS.txt`.
7. **First deploy:** *Actions → Release → Run workflow*, version = the latest release (`v1.0.2` or newer). Approve it when GitHub asks
   (*Review deployments → production → Approve*). It takes about 10 minutes and ends with a green health check.
8. Open `https://app.kordalo.com`, log in as `Administrator` with `ADMIN_PASSWORD`, and complete the setup wizard.

### Optional but recommended (free)
- **UptimeRobot:** HTTP monitor on `https://app.kordalo.com/api/method/ping`, every 5 min.
- **Healthchecks.io:** a check with a 1-day period; put its ping URL in the secret `HEALTHCHECK_URL`
  (applied on the next deploy) to get alerted if a nightly backup doesn't run.
- **Pin the server's host key:** run `ssh-keyscan -t ed25519 <server-ip>` and save the output as the secret
  `DEPLOY_KNOWN_HOSTS`. Without it, deploys trust whatever key the server presents.

---

## Everyday operations

| Task | How |
|---|---|
| Ship a change | PR → green CI → merge → `git tag v1.x.y && git push origin v1.x.y` → approve the deploy |
| Redeploy / roll back to a release | *Actions → Release → Run workflow* with that version |
| Upstream engine update | The weekly *Upstream sync* PR → merge when green → tag a release |
| Change a setting/secret | Update it in GitHub, then redeploy the current version |
| New customer site | `ssh kordalo` → `cd ~/kordalo-deploy && bash scripts/add-site.sh acme.kordalo.com` |
| Logs / status | `ssh kordalo` → `cd ~/kordalo-deploy && docker compose ps` / `docker compose logs -f backend` |
| Disaster recovery | New server (steps 3–4) → `DEPLOY_HOST` = new IP → `ssh kordalo` → `bash ~/kordalo-deploy/scripts/restore.sh` after one deploy run |

`ssh kordalo` works after you add this to `~/.ssh/config` on your PC:
```
Host kordalo
    HostName <server IPv4>
    User kordalo
    IdentityFile ~/.ssh/kordalo_hetzner
```

## What protects uptime
- Every release is fully tested and smoke-tested before it can reach the server; deploys need your approval.
- Each upgrade takes an off-site backup first.
- All containers auto-restart. Swap and capped logs prevent out-of-memory and full-disk crashes.
- Automatic OS security updates, firewall (SSH/HTTP/HTTPS only), key-only SSH, fail2ban.
- Two backup layers: Hetzner daily snapshots plus encrypted nightly restic backups at Backblaze.

## When to grow
- RAM regularly > 80% → resize to CX33/CX43 in the Hetzner console (~2 min downtime).
- Customers need a contractual SLA above 99.5% → multi-server setup with a managed database.
