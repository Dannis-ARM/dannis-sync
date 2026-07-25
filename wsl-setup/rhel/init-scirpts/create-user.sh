#!/bin/bash
# =============================================================================
# Create default user with sudo access
# Usage: CREATE_USER=username bash create-user.sh
# =============================================================================

. "$(dirname "$0")/common.sh"

main() {
    check_root

    local username="${CREATE_USER:-admin_dannis}"

    if ! id "$username" &>/dev/null; then
        log "Creating user $username..."
        useradd -m -c "Admin Dannis" -s /bin/bash -G wheel "$username"
        echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel-nopasswd
        chmod 0440 /etc/sudoers.d/wheel-nopasswd
    else
        log "User $username already exists"
    fi
}

main "$@"
