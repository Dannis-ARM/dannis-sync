@echo off
:: clashon.bat - Turn on proxy using Clash
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
set ALL_PROXY=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
set all_proxy=http://127.0.0.1:7890
set NO_PROXY=localhost,127.0.0.1,::1
set no_proxy=localhost,127.0.0.1,::1

if "%HTTP_PROXY%"=="" (
    echo Proxy Status: OFF
) else (
    echo Proxy Status: ON -^> %HTTP_PROXY%
)