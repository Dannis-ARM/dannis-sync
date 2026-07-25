#!/bin/bash
# =============================================================================
# Common library for WSL init scripts
# =============================================================================

set -euo pipefail

# Constants for terminal colors
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

# Error handling hook for unexpected exits
trap 'error_exit "Script interrupted or failed at line $LINENO"' SIGINT SIGTERM

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%dT%H:%M:%S')] INFO:${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%dT%H:%M:%S')] WARN:${NC} $1"
}

error_exit() {
    echo -e "${RED}[$(date +'%Y-%m-%dT%H:%M:%S')] ERROR:${NC} $1" >&2
    exit 1
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        error_exit "This script must be run as root/sudo."
    fi
}
