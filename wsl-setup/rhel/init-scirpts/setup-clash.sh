#!/bin/bash
# =============================================================================
# Clash Proxy Toggle - Install clashon and clashoff as shell functions
# =============================================================================

set -euo pipefail

PROXY_FUNC_PATH="/usr/local/bin/proxy-functions.sh"

cat > "$PROXY_FUNC_PATH" <<'FUNC_EOF'
# Clash proxy functions - source this file in your ~/.bashrc

get_win_ip() {
    if command -v nslookup &>/dev/null; then
        nslookup "$HOSTNAME" 2>/dev/null | grep Server | awk '{print $2}' | head -1
    else
        grep nameserver /etc/resolv.conf | awk '{print $2}' | head -1
    fi
}

clashon() {
    local WIN_IP=$(get_win_ip)

    if [ -z "$WIN_IP" ]; then
        echo "Error: Could not detect Windows host IP" >&2
        return 1
    fi

    export HTTP_PROXY="http://${WIN_IP}:7890"
    export HTTPS_PROXY="http://${WIN_IP}:7890"
    export http_proxy="http://${WIN_IP}:7890"
    export https_proxy="http://${WIN_IP}:7890"
    export NO_PROXY="localhost,127.0.0.1,::1"
    export no_proxy="localhost,127.0.0.1,::1"

    # Test connection
    echo "Testing connection..."
    if curl -s --connect-timeout 3 https://www.google.com >/dev/null; then
        echo "✓ Proxy enabled: $HTTPS_PROXY"
    else
        echo "✗ Proxy enabled but connection test failed"
        echo "  Check if Clash is running on Windows port 7890"
    fi
}

clashoff() {
    unset HTTP_PROXY
    unset HTTPS_PROXY
    unset http_proxy
    unset https_proxy
    unset NO_PROXY
    unset no_proxy
    echo "Proxy disabled"
}
FUNC_EOF

chmod +x "$PROXY_FUNC_PATH"

# Add to current user's .bashrc if not already there
if [ -n "${SUDO_USER:-}" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    USER_HOME="$HOME"
fi

USER_BASHRC="$USER_HOME/.bashrc"
if [ -f "$USER_BASHRC" ] && ! grep -q "proxy-functions.sh" "$USER_BASHRC"; then
    echo "# Load proxy functions" >> "$USER_BASHRC"
    echo "[ -f $PROXY_FUNC_PATH ] && . $PROXY_FUNC_PATH" >> "$USER_BASHRC"
    echo "Added to $USER_BASHRC"
fi

# Add to skel for new users
mkdir -p /etc/skel
if ! grep -q "proxy-functions.sh" /etc/skel/.bashrc 2>/dev/null; then
    echo "# Load proxy functions" >> /etc/skel/.bashrc
    echo "[ -f $PROXY_FUNC_PATH ] && . $PROXY_FUNC_PATH" >> /etc/skel/.bashrc
fi

echo ""
echo "Then use:"
echo "  clashon  - Enable proxy"
echo "  clashoff - Disable proxy"
