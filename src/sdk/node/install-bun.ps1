$env:HTTPS_PROXY="http://localhost:7890"
cd ~
powershell -c "irm bun.sh/install.ps1 | iex"
# Add-MpPreference -ExclusionPath $(pnpm store path)