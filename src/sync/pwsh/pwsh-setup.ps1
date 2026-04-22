# Configure proxy for localhost:7890
$proxyUri = "http://localhost:7890"
$env:HTTP_PROXY = $proxyUri
$env:HTTPS_PROXY = $proxyUri

Write-Host "🌐 Configured proxy: $proxyUri" -ForegroundColor Green

# Check if scoop is installed
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Scoop is not installed. Please install scoop first: https://scoop.sh/" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Checking PowerShell installation via Scoop..." -ForegroundColor Cyan

# Install pwsh via scoop (idempotent, will skip if already installed)
scoop config proxy 127.0.0.1:7890
scoop install pwsh
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install PowerShell via Scoop" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PowerShell installed successfully via Scoop" -ForegroundColor Green

# Configure PSReadLine with the newly installed pwsh
pwsh -Command "Set-PSReadLineOption -PredictionSource History"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PSReadLine prediction enabled successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️ Failed to configure PSReadLine, you may need to configure it manually" -ForegroundColor Yellow
}
