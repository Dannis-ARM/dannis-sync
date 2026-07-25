$ErrorActionPreference = "Stop"

<#
.SYNOPSIS
Installs and configures Claude Code status line.

.DESCRIPTION
Deploys status_line.py and configures statusLine in settings.local.json.
Supports both project-level (.claude) and user-level (~/.claude) deployment.
Uses python to update JSON (preserves formatting via jq when available).
#>

# Resolve paths
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
$sourcePy = Join-Path $PSScriptRoot "claude-cfgs\status_line\status_line.py"
$userClaudeDir = Join-Path $env:USERPROFILE ".claude"

function Deploy-StatusLine {
    param(
        [Parameter(Mandatory)]
        [string]$ClaudeDir,
        [Parameter(Mandatory)]
        [string]$CommandPath,
        [string]$SettingsFileName = "settings.local.json"
    )

    $targetDir = Join-Path $ClaudeDir "status_lines"
    $targetPy = Join-Path $targetDir "status_line.py"
    $settingsFile = Join-Path $ClaudeDir $SettingsFileName

    # Deploy status_line.py
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Copy-Item $sourcePy $targetPy -Force
    Write-Host "Deployed status_line.py -> $targetPy"

    # Use Python to update JSON - simple and reliable
    $pythonScript = @"
import json, sys, os
settings_file = r'$settingsFile'
cmd = r'$CommandPath'

if os.path.exists(settings_file):
    with open(settings_file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
else:
    data = {}

data['statusLine'] = {'type': 'command', 'command': cmd, 'padding': 0}

with open(settings_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
"@
    $pythonScript | python -
    Write-Host "Configured statusLine in $settingsFile"
}

# Check dependencies
if (-not (Test-Path $sourcePy)) {
    Write-Error "Source not found: $sourcePy"
    exit 1
}
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Error "python not found"
    exit 1
}

# Deploy to both locations
Deploy-StatusLine `
    -ClaudeDir (Join-Path $projectRoot ".claude") `
    -CommandPath "uv run `$CLAUDE_PROJECT_DIR/.claude/status_lines/status_line.py" `
    -SettingsFileName "settings.local.json"

Deploy-StatusLine `
    -ClaudeDir $userClaudeDir `
    -CommandPath "uv run ~/.claude/status_lines/status_line.py" `
    -SettingsFileName "settings.json"

Write-Host ""
Write-Host "Status line installed successfully"
