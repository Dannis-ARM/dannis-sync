#!/bin/bash
# =============================================================================
# Rocky Linux 9 System Initialization Script
# Version: 2.2
# =============================================================================

set -euo pipefail

# Constants for terminal colors
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

# Error handling hook for unexpected exits
trap 'error_exit "Script interrupted or failed at line $LINENO"' SIGINT SIGTERM

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%dT%H:%M:%S')] INFO:${NC} $1"
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

enable_repos() {
    # Ensure dnf-plugins-core is installed before using config-manager
    if ! rpm -q dnf-plugins-core &>/dev/null; then
        log "Installing dnf-plugins-core..."
        dnf install -y dnf-plugins-core || error_exit "Failed to install dnf-plugins-core."
    fi

    if ! dnf repolist enabled | grep -q "^crb"; then
        log "Enabling CRB repository..."
        dnf config-manager --set-enabled crb || error_exit "Failed to enable CRB repo."
    fi

    if ! rpm -q epel-release &>/dev/null; then
        log "Installing EPEL repository..."
        dnf install -y epel-release || error_exit "Failed to install EPEL."
    fi
}

update_packages() {
    log "Updating dnf package index..."
    dnf makecache || error_exit "Failed to update dnf index."
}

install_tools() {
    # Grouping all packages into a single transaction for better performance
    local -r packages=(
        net-tools cronie htop sysstat zip unzip git make jq tar
        vim-enhanced # Replaced vim-minimal
        nmap-ncat    # Replaced nc
        mtr
        fuse-overlayfs podman podman-docker
    )
    
    log "Installing system, network, and container tools..."
    dnf install -y "${packages[@]}" || error_exit "Failed to install tools."
}

config_system() {
    log "Configuring system timezone..."
    if [[ -f /run/systemd/system ]]; then
        timedatectl set-timezone Asia/Shanghai || log "Warning: Failed to set timezone via timedatectl."
    else
        ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    fi

    log "Ensuring crond service is enabled..."
    if command -v systemctl &>/dev/null && [[ -d /run/systemd/system ]]; then
        systemctl enable --now crond 2>/dev/null || log "Warning: Failed to start crond via systemctl."
    fi
}

cleanup() {
    log "Cleaning up dnf cache..."
    dnf autoremove -y && dnf clean all
}

main() {
    log "Starting system initialization..."

    check_root
    enable_repos
    update_packages
    install_tools
    config_system
    cleanup

    log "System initialization completed successfully!"
}

# Execute main function
main "$@"