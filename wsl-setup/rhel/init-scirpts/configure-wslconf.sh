#!/bin/bash
# =============================================================================
# Configure WSL /etc/wsl.conf to disable Windows PATH interop
# Version: 1.1
# =============================================================================

configure_wsl_conf() {
    local wsl_conf="/etc/wsl.conf"

    log "Configuring WSL interop settings..."

    # Check if file exists
    if [[ -f "$wsl_conf" ]]; then
        warn "$wsl_conf already exists. Checking for existing [interop] section..."

        # Backup existing config
        cp "$wsl_conf" "${wsl_conf}.bak.$(date +%Y%m%d%H%M%S)"
        log "Backup created at ${wsl_conf}.bak.$(date +%Y%m%d%H%M%S)"
    fi

    # Use a temporary file to build the new config
    local temp_file=$(mktemp)

    # If file exists, copy all sections except [interop]
    if [[ -f "$wsl_conf" ]]; then
        awk '
            BEGIN { in_interop = 0 }
            /^\[interop\]/ { in_interop = 1; next }
            /^\[/ && in_interop { in_interop = 0 }
            !in_interop { print }
        ' "$wsl_conf" > "$temp_file"
    fi

    # Append our [interop] section
    cat >> "$temp_file" << 'WSL_CONF'

[boot]
systemd=true

[interop]
enabled = true
appendWindowsPath = false
WSL_CONF

    # Move temp file to final location
    mv "$temp_file" "$wsl_conf"
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
