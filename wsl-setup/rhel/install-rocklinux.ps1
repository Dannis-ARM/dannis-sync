#Requires -RunAsAdministrator

param(
    [string]$DistroName = "Rocky-9",
    [string]$InstallDir = "$env:LOCALAPPDATA\WSL\$DistroName",
    [string]$DownloadDir = "$env:LOCALAPPDATA\WSL",
    [string]$ImageUrl = "https://dl.rockylinux.org/pub/rocky/9/images/x86_64/Rocky-9-WSL-Base.latest.x86_64.wsl",
    [string]$DefaultUser = "admin_dannis"
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

# Import and configure
Write-Host "Importing $DistroName..."
wsl --import $DistroName $InstallDir $imagePath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to import distro (code $LASTEXITCODE)"
    exit 1
}

# Enable systemd and create user
wsl -d $DistroName -u root bash -c @"
cat > /etc/wsl.conf << 'EOF'
[boot]
systemd=true
EOF
if ! id '$DefaultUser' &>/dev/null; then
    useradd -m -c 'Admin Dannis' -s /bin/bash -G wheel '$DefaultUser'
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel-nopasswd
    chmod 0440 /etc/sudoers.d/wheel-nopasswd
fi
"@
if ($LASTEXITCODE -ne 0) {
    Write-Error "Configuration failed (code $LASTEXITCODE)"
    exit 1
}

# Restart and set default user
wsl -t $DistroName
Start-Sleep -Seconds 2
wsl --manage $DistroName --set-default-user $DefaultUser

Write-Host "Done! Use 'wsl -d $DistroName' to start."
wsl --list --verbose
