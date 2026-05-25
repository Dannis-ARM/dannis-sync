$env:HTTPS_PROXY="http://localhost:7890"

# Check if already installed
if (Get-Command "bun" -ErrorAction SilentlyContinue) {
    Write-Host "bun already installed"; bun --version; exit 0
}

cd ~
powershell -c "irm bun.sh/install.ps1 | iex"
# Add-MpPreference -ExclusionPath $(pnpm store path)