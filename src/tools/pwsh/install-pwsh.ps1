# 1. 环境与代理 (一行流)
$env:HTTP_PROXY = $env:HTTPS_PROXY = "http://127.0.0.1:7890"
if (!(Get-Command scoop -ErrorAction SilentlyContinue)) { throw "Scoop missing" }

# 2. 安装并锁定版本
# 使用 -s (skip) 检查是否已安装且版本匹配，避免重复安装
if (!(scoop list pwsh | Select-String "7.6.1")) {
    Write-Host "🔍 Installing pwsh 7.6.1..." -ForegroundColor Cyan
    scoop config proxy 127.0.0.1:7890
    scoop install pwsh@7.6.1
    scoop hold pwsh
}

# 3. 幂等配置 PSReadLine (核心优化)
# 预计算路径，避免调用 pwsh.exe 产生的额外开销
$profilePath = "$Home\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
$configBlock = @"

# PSReadLine Optimization
Import-Module PSReadLine -ErrorAction SilentlyContinue
Set-PSReadLineOption -PredictionSource History
"@

# 确保目录存在
$null = New-Item -Path (Split-Path $profilePath) -ItemType Directory -Force

# 幂等写入：如果文件中不包含配置，则追加
if (!(Test-Path $profilePath) -or !(Select-String "PredictionSource History" $profilePath -SimpleMatch)) {
    $configBlock | Add-Content -Path $profilePath
    Write-Host "✅ Profile updated: $profilePath" -ForegroundColor Green
} else {
    Write-Host "✨ Profile already configured." -ForegroundColor Gray
}