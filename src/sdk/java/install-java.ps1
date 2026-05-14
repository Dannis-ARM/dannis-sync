### 优化后的幂等性脚本 ###

# 1. 配置代理 (覆盖操作，天然幂等)
scoop config proxy 127.0.0.1:7890

# 2. 配置 aria2 (覆盖操作，天然幂等)
scoop config aria2-enabled true
scoop config aria2-max-connection-per-server 16
scoop config aria2-split 32
scoop config aria2-min-split-size 1M
scoop config aria2-retry-wait 4

# 3. 幂等添加 Bucket
$buckets = scoop bucket list
if ($buckets -notcontains 'java') {
    Write-Host "Adding java bucket..." -ForegroundColor Cyan
    scoop bucket add java
}

# 4. 幂等安装软件包函数
function Safe-ScoopInstall($app) {
    $localApps = scoop list
    if ($localApps -like "*$app*") {
        Write-Host "App [$app] is already installed. Skipping..." -ForegroundColor Yellow
    } else {
        Write-Host "Installing [$app]..." -ForegroundColor Green
        scoop install $app
    }
}

# 执行安装
Safe-ScoopInstall "aria2"
Safe-ScoopInstall "temurin8-jdk"
Safe-ScoopInstall "temurin21-jdk"

# 5. 关于版本切换 (reset)
# scoop reset 本身是幂等的，它会重新建立环境变量和 Shim
# 但通常建议只在需要切换时手动执行
# scoop reset temurin21-jdk