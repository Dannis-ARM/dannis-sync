#!/bin/bash
# 获取脚本所在目录的绝对路径，确保能找到 py 脚本
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 执行 py 脚本并 eval 其输出
eval "$(python3 "$DIR/setproxy.py" --quiet "$@")"

if [ -z "$HTTP_PROXY" ]; then
    echo "Proxy Status: OFF"
else
    echo "Proxy Status: ON -> $HTTP_PROXY"
fi