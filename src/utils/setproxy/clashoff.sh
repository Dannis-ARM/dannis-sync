#!/bin/bash
# clashoff.sh - Turn off proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
unset http_proxy
unset https_proxy
unset all_proxy
unset NO_PROXY
unset no_proxy

if [ -z "$HTTP_PROXY" ]; then
    echo "Proxy Status: OFF"
else
    echo "Proxy Status: ON -> $HTTP_PROXY"
fi