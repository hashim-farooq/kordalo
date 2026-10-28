# Run on your Windows PC: creates your SSH key (if missing) and cloud-init.generated.yaml,
# which authorises both your key and the GitHub Actions deploy key on the new server.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$key = Join-Path $env:USERPROFILE '.ssh\kordalo_hetzner'

if (-not (Test-Path $key)) {
    New-Item -ItemType Directory -Force (Split-Path $key) | Out-Null
    Write-Host 'Creating SSH key. Choose a passphrase you will remember (or press Enter twice for none).'
    ssh-keygen -t ed25519 -f $key -C 'kordalo-admin'
}

$pub = (Get-Content "$key.pub" -Raw).Trim()
$deploy = (Get-Content (Join-Path $root 'ci-deploy.pub') -Raw).Trim()
$template = Get-Content (Join-Path $root 'cloud-init.yaml') -Raw
$out = Join-Path $root 'cloud-init.generated.yaml'
$text = $template.Replace('__SSH_PUBLIC_KEY__', $pub).Replace('__DEPLOY_PUBLIC_KEY__', $deploy).Replace("`r`n", "`n")
[IO.File]::WriteAllText($out, $text)

Set-Clipboard -Value $text
Write-Host "Done. $out has been copied to your clipboard."
Write-Host 'Paste it into the "Cloud config" box when creating the Hetzner server.'
