# 1. 统一代理配置
$proxyAddr = "http://127.0.0.1:7890"
$env:HTTP_PROXY = $env:HTTPS_PROXY = "http://127.0.0.1:7890"
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxyAddr)

# 1. 检查是否已安装
if (Get-Command "gh" -ErrorAction SilentlyContinue) { 
    gh --version; exit 0 
}

if (-not (Get-Command "scoop" -ErrorAction SilentlyContinue)) {
    Write-Error "Scoop missing. Install it first: https://scoop.sh/"; exit 1
}

# 3. 安装并验证
Write-Host "Installing GitHub CLI..."
scoop install gh

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Success"
    gh --version
} else {
    Write-Error "❌ Failed"
    exit 1
}
