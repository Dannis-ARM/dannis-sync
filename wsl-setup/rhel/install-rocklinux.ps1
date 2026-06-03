#Requires -RunAsAdministrator

param(
    [string]$DistroName = "Rocky-9",
    [string]$InstallDir = "$env:LOCALAPPDATA\WSL\$DistroName",
    [string]$DownloadDir = "$env:LOCALAPPDATA\WSL",
    [string]$ImageUrl = "https://dl.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-WSL-Base.latest.x86_64.wsl"
)

$ErrorActionPreference = "Stop"
$imagePath = Join-Path $DownloadDir "Rocky-9-WSL-Base.latest.x86_64.wsl"

function Test-DistroExists {
    param($Name)
    $distros = wsl --list --quiet 2>$null
    if ($LASTEXITCODE -ne 0) { return $false }
    $distros -contains $Name
}

# Ensure directories
foreach ($dir in ($DownloadDir, $InstallDir)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}

# Download image
if (-not (Test-Path $imagePath)) {
    Write-Host "Downloading Rocky Linux 9..."
    if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
        curl.exe -L -o $imagePath $ImageUrl
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Download failed with code $LASTEXITCODE"
            if (Test-Path $imagePath) { Remove-Item $imagePath -Force }
            exit 1
        }
    } else {
        Invoke-WebRequest -Uri $ImageUrl -OutFile $imagePath -UseBasicParsing
    }
}

# Verify image exists
if (-not (Test-Path $imagePath)) {
    Write-Error "Image file not found: $imagePath"
    exit 1
}

# Check existing distro
if (Test-DistroExists $DistroName) {
    Write-Host "Distro '$DistroName' already exists."
    exit 0
}

# Import distro
Write-Host "Importing $DistroName..."
wsl --import $DistroName $InstallDir $imagePath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to import distro (code $LASTEXITCODE)"
    exit 1
}

Write-Host "Done! Distro '$DistroName' imported."
Write-Host "Next step: run .\rockylinux-init.ps1 to initialize."
wsl --list --verbose
