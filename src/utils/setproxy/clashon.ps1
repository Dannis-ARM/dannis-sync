# clashon.ps1 - Turn on proxy using Clash
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
$env:ALL_PROXY = "http://127.0.0.1:7890"
$env:http_proxy = "http://127.0.0.1:7890"
$env:https_proxy = "http://127.0.0.1:7890"
$env:all_proxy = "http://127.0.0.1:7890"
$env:NO_PROXY = "localhost,127.0.0.1,::1"
$env:no_proxy = "localhost,127.0.0.1,::1"

if ($env:HTTP_PROXY -eq "") {
    Write-Host "Proxy Status: OFF"
} else {
    Write-Host "Proxy Status: ON -> $env:HTTP_PROXY"
}