# clashoff.ps1 - Turn off proxy
$env:HTTP_PROXY = $null
$env:HTTPS_PROXY = $null
$env:ALL_PROXY = $null
$env:http_proxy = $null
$env:https_proxy = $null
$env:all_proxy = $null
$env:NO_PROXY = $null
$env:no_proxy = $null

if ($env:HTTP_PROXY -eq "") {
    Write-Host "Proxy Status: OFF"
} else {
    Write-Host "Proxy Status: ON -> $env:HTTP_PROXY"
}