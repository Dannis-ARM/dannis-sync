$env:HTTPS_PROXY="http://localhost:7890"
cd ~
iwr https://get.pnpm.io/install.ps1 -UseBasicParsing | Invoke-Expression
# Add-MpPreference -ExclusionPath $(pnpm store path)