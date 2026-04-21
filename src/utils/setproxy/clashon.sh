#!/bin/bash
# clashon.sh - Turn on proxy using Clash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export ALL_PROXY="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export all_proxy="http://127.0.0.1:7890"
export NO_PROXY="localhost,127.0.0.1,::1"
export no_proxy="localhost,127.0.0.1,::1"

if [ -z "$HTTP_PROXY" ]; then
    echo "Proxy Status: OFF"
else
    echo "Proxy Status: ON -> $HTTP_PROXY"
fi