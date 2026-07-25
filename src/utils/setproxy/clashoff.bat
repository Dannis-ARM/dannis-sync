@echo off
:: clashoff.bat - Turn off proxy
set HTTP_PROXY=
set HTTPS_PROXY=
set ALL_PROXY=
set http_proxy=
set https_proxy=
set all_proxy=
set NO_PROXY=
set no_proxy=

if "%HTTP_PROXY%"=="" (
    echo Proxy Status: OFF
) else (
    echo Proxy Status: ON -^> %HTTP_PROXY%
)