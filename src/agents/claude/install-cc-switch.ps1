$ErrorActionPreference = "Stop"

# cc-switch github: https://github.com/farion1231/cc-switch
$version = "3.15.0"
$url = "https://github.com/farion1231/cc-switch/releases/download/v$version/CC-Switch-v$version-Windows-Portable.zip"
$targetDir = Join-Path $env:APPDATA "CC-Switch"
$zipPath = Join-Path $env:TEMP "CC-Switch.zip"

$proxy = "http://127.0.0.1:7890"
$env:HTTP_PROXY = $env:HTTPS_PROXY = $proxy

# 检查是否已安装该版本或更新版本
$versionFile = Join-Path $targetDir "version.txt"
if (Test-Path $versionFile) {
    $installedVersion = Get-Content $versionFile
    if ($installedVersion -eq $version) {
        Write-Host "CC-Switch v$version already installed"
        exit 0
    }
    try {
        $installedVer = [version]$installedVersion
        $targetVer = [version]$version
        if ($installedVer -ge $targetVer) {
            Write-Host "CC-Switch v$installedVersion already installed (newer than or equal to v$version)"
            exit 0
        }
    } catch {
        Write-Host "Warning: Could not compare versions, proceeding with install..."
    }
}

Write-Host "Downloading..."
Invoke-WebRequest $url -OutFile $zipPath -Proxy $proxy -UseBasicParsing

Write-Host "Extracting to $targetDir..."
if (Test-Path $targetDir) { Remove-Item $targetDir -Recurse -Force }
Expand-Archive $zipPath $targetDir -Force

$version | Out-File $versionFile -Encoding utf8

Remove-Item $zipPath -Force
Write-Host "Done"
