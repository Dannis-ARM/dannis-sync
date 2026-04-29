<#
.SYNOPSIS
    自动化安装并锁定特定版本的 pwsh，并配置持久化 PSReadLine 预测。
#>

# 1. 统一代理配置 (修正变量名错误)
$proxyAddr = "http://127.0.0.1:7890"
$env:HTTP_PROXY  = $proxyAddr
$env:HTTPS_PROXY = $proxyAddr
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxyAddr)

Write-Host "🌐 Configured proxy: $proxyAddr" -ForegroundColor Green

# 2. 环境检查
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Scoop is not installed." -ForegroundColor Red
    exit 1
}

# 3. Scoop 配置与安装
Write-Host "🔍 Installing PowerShell 7.6.1 via Scoop..." -ForegroundColor Cyan
scoop config proxy "127.0.0.1:7890"

# 增加 --global 提示或显式指定 bucket (如果需要 versions)
# 注意：如果 7.6.1 不在 main bucket，请先 scoop bucket add versions
scoop install pwsh@7.6.1
if ($LASTEXITCODE -eq 0) {
    scoop hold pwsh
    Write-Host "✅ PowerShell 7.6.1 installed and held." -ForegroundColor Green
} else {
    Write-Error "❌ Failed to install pwsh@7.6.1"
    exit 1
}

# 4. 持久化配置 PSReadLine (核心优化)
Write-Host "📝 Configuring PSReadLine prediction in Profile..." -ForegroundColor Cyan

# 定义要注入 Profile 的配置行
$profileConfig = "`nImport-Module PSReadLine`nSet-PSReadLineOption -PredictionSource History"

# 针对新安装的 pwsh (PowerShell Core) 的 Profile 路径
$pwshProfilePath = pwsh -Command "echo `$PROFILE"

if ($null -ne $pwshProfilePath) {
    $profileDir = Split-Path $pwshProfilePath
    if (-not (Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir -Force }
    if (-not (Test-Path $pwshProfilePath)) { New-Item -ItemType File -Path $pwshProfilePath -Force }
    
    # 避免重复追加
    if ((Get-Content $pwshProfilePath) -notcontains "Set-PSReadLineOption -PredictionSource History") {
        Add-Content -Path $pwshProfilePath -Value $profileConfig
        Write-Host "✅ Persistent configuration added to $pwshProfilePath" -ForegroundColor Green
    }
}