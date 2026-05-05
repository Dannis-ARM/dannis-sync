Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 1. 统一代理配置 (修正变量名错误)
$proxyAddr = "http://127.0.0.1:7890"
$env:HTTP_PROXY  = $proxyAddr
$env:HTTPS_PROXY = $proxyAddr
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($proxyAddr)

irm -Proxy 'http://127.0.0.1:7890' https://claude.ai/install.ps1 | iex

# get cc switch | otherwise you cannot login to CC
# https://github.com/farion1231/cc-switch