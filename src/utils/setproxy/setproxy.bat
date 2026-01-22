@echo off
:: use 'for' to capture python output and execute
for /f "tokens=*" %%i in ('python "%~dp0setproxy.py" --quiet %*') do (
    %%i
)

if "%HTTP_PROXY%"=="" (
    echo Proxy Status: OFF
) else (
    echo Proxy Status: ON -^> %HTTP_PROXY%
)