$ErrorActionPreference = "Stop"

# Resolve paths
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$sourcePy = Join-Path $PSScriptRoot "claude-cfgs\status_line\status_line.py"
$targetDir = Join-Path $projectRoot ".claude\status_lines"
$targetPy = Join-Path $targetDir "status_line.py"
$settingsFile = Join-Path $projectRoot ".claude\settings.local.json"

# Step 1: Deploy status_line.py
if (-not (Test-Path $sourcePy)) {
    Write-Error "Source not found: $sourcePy"
    exit 1
}

New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Copy-Item $sourcePy $targetPy -Force
Write-Host "Deployed status_line.py -> $targetPy"

# Step 2: Configure statusLine in settings.local.json
$statusLineConfig = @{
    type    = "command"
    command = "uv run `$CLAUDE_PROJECT_DIR/.claude/status_lines/status_line.py"
    padding = 0
}

if (Test-Path $settingsFile) {
    $json = Get-Content $settingsFile -Raw
    $settings = ConvertFrom-Json $json
} else {
    $settings = [PSCustomObject]@{}
}

# Overwrite statusLine property
$settings | Add-Member -NotePropertyName "statusLine" -NotePropertyValue $statusLineConfig -Force

# Write back (depth 10 to handle nested objects)
$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsFile -Encoding utf8
Write-Host "Configured statusLine in $settingsFile"
