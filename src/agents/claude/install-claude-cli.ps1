$ErrorActionPreference = "Stop"

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

$proxy = "http://127.0.0.1:7890"
$env:HTTP_PROXY = $env:HTTPS_PROXY = $proxy
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxy)

# Install Claude CLI
irm -Proxy $proxy https://claude.ai/install.ps1 | iex

# Install CC-Switch
$scriptPath = Join-Path $PSScriptRoot "install-cc-switch.ps1"
& $scriptPath
