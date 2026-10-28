# Step 1 (on your Windows PC): creates an SSH key and the cloud-init config for Hetzner.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$key = Join-Path $env:USERPROFILE '.ssh\kordalo_hetzner'

if (-not (Test-Path $key)) {
    New-Item -ItemType Directory -Force (Split-Path $key) | Out-Null
    Write-Host 'Creating SSH key. Choose a passphrase you will remember (or press Enter twice for none).'
    ssh-keygen -t ed25519 -f $key -C 'kordalo-hetzner'
}

$pub = (Get-Content "$key.pub" -Raw).Trim()
$template = Get-Content (Join-Path $root 'cloud-init.yaml') -Raw
$out = Join-Path $root 'cloud-init.generated.yaml'
[IO.File]::WriteAllText($out, $template.Replace('__SSH_PUBLIC_KEY__', $pub).Replace("`r`n", "`n"))

Set-Clipboard -Value (Get-Content $out -Raw)
Write-Host ''
Write-Host "Done. $out has been copied to your clipboard."
Write-Host 'Paste it into the "Cloud config" box when creating the Hetzner server.'
