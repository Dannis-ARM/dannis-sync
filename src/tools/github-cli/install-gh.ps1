# 🧐 Check if GitHub CLI (gh) is already installed
$ghExists = Get-Command "gh" -ErrorAction SilentlyContinue
if ($ghExists) {
    Write-Host "✅ GitHub CLI is already installed:"
    gh --version
    exit 0
}

Write-Host "⚙️ GitHub CLI not found, starting installation..."

# 1. 统一代理配置
$proxyAddr = "http://127.0.0.1:7890"
$env:HTTP_PROXY  = $proxyAddr
$env:HTTPS_PROXY = $proxyAddr
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxyAddr)

# 2. Check if scoop is available
$scoopExists = Get-Command "scoop" -ErrorAction SilentlyContinue
if (-not $scoopExists) {
    Write-Host "❌ Installation failed: scoop is not installed"
    Write-Host "💡 Please install scoop first:"
    Write-Host "   - Run: src/sdk/install-scoop.ps1"
    Write-Host "   - Or visit: https://scoop.sh/"
    exit 1
}

# 3. Install GitHub CLI via scoop
scoop install gh

# 4. Verify installation
$ghInstalled = Get-Command "gh" -ErrorAction SilentlyContinue
if ($ghInstalled) {
    Write-Host "✅ GitHub CLI installed successfully:"
    gh --version
    exit 0
} else {
    Write-Host "❌ GitHub CLI installation failed!"
    exit 1
}
