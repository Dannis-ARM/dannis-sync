@echo off
setlocal enabledelayedexpansion

:: 🧐 Check if uv is already installed
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ uv is already installed:
    uv --version
    exit /b 0
)

echo ⚙️ uv not found, starting installation...

:: Set proxy for installation
set HTTPS_PROXY=http://127.0.0.1:7890

:: Install uv via official script
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

:: Verify installation after install
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ uv installed successfully:
    uv --version
    exit /b 0
) else (
    echo ❌ uv installation failed!
    echo 💡 Alternative installation method if you have pipx already:
    echo    pipx install uv
    exit /b 1
)
