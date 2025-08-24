@echo off
:: 本脚本仅在 Windows cmd 下有效，环境变量仅在本会话生效。
:: 若需永久设置，请参考相关配置文件说明。
echo Setting up temporary mirrors for Python, Java, and Node.js...

:: 保存原始环境变量
set "ORIGINAL_PIP_INDEX_URL=%PIP_INDEX_URL%"
set "ORIGINAL_PIP_TRUSTED_HOST=%PIP_TRUSTED_HOST%"
set "ORIGINAL_NPM_CONFIG_REGISTRY=%npm_config_registry%"

:: 检查 pip 是否安装
where pip >nul 2>nul || echo [警告] pip 未安装
:: 检查 npm 是否安装
where npm >nul 2>nul || echo [警告] npm 未安装

:: --- Python (pip) ---
echo.
echo Setting Python (pip) mirror...
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
set PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
echo [提示] 仅在本会话有效。如需永久设置，请修改 pip.ini。
echo You can now use "pip install" within this script.
echo For example: pip install numpy

:: --- Node.js (npm) ---
echo.
echo Setting Node.js (npm) mirror...
set npm_config_registry=https://registry.npmmirror.com
echo [提示] 仅在本会话有效。如需永久设置，请修改 .npmrc。
echo You can now use "npm install" within this script.
echo For example: npm install express

:: --- 进入新的命令行会话 ---
echo.
echo Entering a new command prompt session with temporary settings.
echo Type "exit" to return to the parent script.
cmd.exe /k "echo Welcome to your temporary mirrored shell."

echo.
echo Exiting the temporary mirrored shell.
echo The mirrors for Python and Node.js are no longer active.

:: 恢复原始环境变量
echo Restoring original environment variables...
set "PIP_INDEX_URL=%ORIGINAL_PIP_INDEX_URL%"
set "PIP_TRUSTED_HOST=%ORIGINAL_PIP_TRUSTED_HOST%"
set "npm_config_registry=%ORIGINAL_NPM_CONFIG_REGISTRY%"

:: 清除临时变量
set "ORIGINAL_PIP_INDEX_URL="
set "ORIGINAL_PIP_TRUSTED_HOST="
set "ORIGINAL_NPM_CONFIG_REGISTRY="

pause
