#!/bin/bash
# =============================================================================
# Configure WSL /etc/wsl.conf to disable Windows PATH interop
# Version: 1.3
# =============================================================================

. "$(dirname "$0")/common.sh"

configure_wsl_conf() {
    local wsl_conf="/etc/wsl.conf"

    log "Configuring WSL interop settings..."

    # Backup if exists
    if [[ -f "$wsl_conf" ]]; then
        cp "$wsl_conf" "${wsl_conf}.bak.$(date +%Y%m%d%H%M%S)"
        log "Backup created at ${wsl_conf}.bak.$(date +%Y%m%d%H%M%S)"
    fi

    # Write complete config
    cat > "$wsl_conf" << 'WSL_CONF'
[boot]
systemd=true

[interop]
enabled = true
appendWindowsPath = false
WSL_CONF

    chmod 644 "$wsl_conf"

    log "WSL configuration updated successfully!"
    log "  - boot.systemd = true"
    log "  - interop.enabled = true (keeps Windows executable support)"
    log "  - interop.appendWindowsPath = false (disables Windows PATH injection)"
    log ""
    log "NOTE: You need to shutdown WSL for changes to take effect:"
    log "      From Windows (PowerShell/Command Prompt):"
    log "        wsl --shutdown"
    log "      Then restart your WSL distribution."
}

main() {
    log "Starting WSL configuration..."

    check_root
    configure_wsl_conf

    log "WSL configuration completed!"
}

main "$@"
