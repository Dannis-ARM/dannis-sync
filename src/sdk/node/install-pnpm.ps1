$env:HTTPS_PROXY="http://localhost:7890"

# Check if already installed
if (Get-Command "pnpm" -ErrorAction SilentlyContinue) {
    Write-Host "pnpm already installed"; pnpm --version; exit 0
}

cd ~
iwr https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression
# Add-MpPreference -ExclusionPath $(pnpm store path)