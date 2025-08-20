@echo off
echo Setting up temporary mirrors for Python, Java, and Node.js...

:: --- Python (pip) ---
echo.
echo Setting Python (pip) mirror...
set PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
set PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
echo You can now use "pip install" within this script.
echo For example: pip install numpy

:: --- Node.js (npm) ---
echo.
echo Setting Node.js (npm) mirror...
set npm_config_registry=https://registry.npmmirror.com
echo You can now use "npm install" within this script.
echo For example: npm install express

:: --- Java (Maven) ---
echo.
echo Setting Java (Maven) mirror...
:: Note: Maven's mirror setting is more complex and typically requires modifying the settings.xml file.
:: This script will not change the global settings. Instead, we can use the -Dmaven.wagon.http.proxyHost and similar flags.
:: Or, more simply, you can modify the settings.xml file for your project.
:: The following command will NOT work without project-level settings.xml.
echo This script does NOT set a global Maven mirror.
echo It's recommended to configure your project's pom.xml or a local settings.xml.
echo For example, in your settings.xml:
echo ^<mirror^>
echo   ^<id^>aliyun^</id^>
echo   ^<mirrorOf^>*^</mirrorOf^>
echo   ^<url^>https://maven.aliyun.com/nexus/content/groups/public/^</url^>
echo ^</mirror^>

:: --- Entering a new command prompt session ---
echo.
echo Entering a new command prompt session with temporary settings.
echo Type "exit" to return to the parent script.
cmd.exe /k "echo Welcome to your temporary mirrored shell."

echo.
echo Exiting the temporary mirrored shell.
echo The mirrors for Python and Node.js are no longer active.
pause