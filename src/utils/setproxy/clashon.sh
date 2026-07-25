#!/bin/bash
# clashon.sh - Turn on proxy using Clash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export ALL_PROXY="http://127.0.0.1:7890"
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export all_proxy="http://127.0.0.1:7890"

# NO_PROXY - Domains that bypass proxy
NO_PROXY_LIST=(
    "localhost" "127.0.0.1" "::1"
    ".cn"
    ".baidu.com"
    ".aliyuncs.com" ".aliyun.com" ".alibaba.com" ".taobao.com" ".tmall.com"
    ".163.com" ".netease.com"
    ".qq.com" ".tencent.com" ".weixin.qq.com" ".wechat.com"
    ".sina.com.cn" ".weibo.com"
    ".zhihu.com" ".bilibili.com" ".jd.com" ".pinduoduo.com"
    ".meituan.com" ".dianping.com"
    ".bytedance.com" ".toutiao.com" ".douyin.com" ".volces.com" ".ark.cn-beijing.volcesapi.com"
    ".tsinghua.edu.cn" ".edu.cn" ".ac.cn"
    ".xiaomi.com" ".huawei.com"
)
# Join array with commas
IFS=,
export NO_PROXY="${NO_PROXY_LIST[*]}"
export no_proxy="$NO_PROXY"
unset IFS

if [ -z "$HTTP_PROXY" ]; then
    echo "Proxy Status: OFF"
else
    echo "Proxy Status: ON -> $HTTP_PROXY"
fi