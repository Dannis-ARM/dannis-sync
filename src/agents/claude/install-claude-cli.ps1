$ErrorActionPreference = "Stop"

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

$proxy = "http://127.0.0.1:7890"
$env:HTTP_PROXY = $env:HTTPS_PROXY = $proxy
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxy)

# Check if already installed
if (Get-Command "claude" -ErrorAction SilentlyContinue) {
    Write-Host "Claude CLI already installed"
    claude --version
} else {
    # Install Claude CLI
    Write-Host "Installing Claude CLI..."
    irm -Proxy $proxy https://claude.ai/install.ps1 | iex
}

# Install CC-Switch (handles its own precheck)
$scriptPath = Join-Path $PSScriptRoot "install-cc-switch.ps1"
& $scriptPath
