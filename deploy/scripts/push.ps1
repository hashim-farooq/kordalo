# Copies the deploy kit (including your filled-in .env) to the server and adds a
# "kordalo" shortcut so you can connect with just:  ssh kordalo
# Usage: .\scripts\push.ps1 -ServerIp 1.2.3.4
param([Parameter(Mandatory)][string]$ServerIp)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$key = Join-Path $env:USERPROFILE '.ssh\kordalo_hetzner'
$sshConfig = Join-Path $env:USERPROFILE '.ssh\config'

if (-not (Test-Path (Join-Path $root '.env'))) { throw 'Create .env first: copy .env.example to .env and fill it in.' }

$entry = "`nHost kordalo`n    HostName $ServerIp`n    User kordalo`n    IdentityFile $key`n"
if (-not ((Test-Path $sshConfig) -and (Select-String -Path $sshConfig -Pattern '^Host kordalo$' -Quiet))) {
    Add-Content -Path $sshConfig -Value $entry -Encoding ascii
} else {
    Write-Host "Note: 'Host kordalo' already in $sshConfig - make sure its HostName is $ServerIp."
}

ssh kordalo 'mkdir -p ~/kordalo-deploy/scripts'
scp (Join-Path $root 'compose.yaml') (Join-Path $root 'Caddyfile') (Join-Path $root '.env') (Join-Path $root '.env.example') kordalo:kordalo-deploy/
scp (Get-ChildItem (Join-Path $root 'scripts\*.sh')).FullName kordalo:kordalo-deploy/scripts/
ssh kordalo "sed -i 's/\r$//' ~/kordalo-deploy/scripts/*.sh ~/kordalo-deploy/Caddyfile ~/kordalo-deploy/compose.yaml; chmod 600 ~/kordalo-deploy/.env"
Write-Host 'Uploaded. Next: ssh kordalo   then   bash ~/kordalo-deploy/scripts/deploy.sh'
