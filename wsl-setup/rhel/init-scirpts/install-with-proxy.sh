#!/bin/bash
# =============================================================================
# Install packages with proxy enabled
# Version: 2.4
# =============================================================================

. "$(dirname "$0")/common.sh"

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
    check_root

    # Source proxy functions
    if [ -f /usr/local/bin/proxy-functions.sh ]; then
        . /usr/local/bin/proxy-functions.sh
        clashon || exit 1
    else
        warn "Proxy functions not found, proceeding without proxy"
    fi

    log "Starting system initialization..."
    enable_repos
    update_packages
    install_tools
    config_system
    cleanup
    log "System initialization completed successfully!"
}

main "$@"
