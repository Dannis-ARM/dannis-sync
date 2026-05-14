# 1. 强制内存代理（无视环境变量缓存）
$proxyAddr = "http://127.0.0.1:7890"
$env:HTTP_PROXY = $proxyUri
$env:HTTPS_PROXY=$proxyAddr
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxyAddr)

# Check if scoop is already installed
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Host "Scoop not found, starting installation..."
    irm get.scoop.sh -Proxy 'http://127.0.0.1:7890' | iex
    Write-Host "Scoop installed successfully!"
} else {
    Write-Host "Scoop is already installed, skipping installation."
}

scoop config proxy 127.0.0.1:7890