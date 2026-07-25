# clashon.ps1 - Turn on proxy using Clash
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
$env:ALL_PROXY = "http://127.0.0.1:7890"
$env:http_proxy = "http://127.0.0.1:7890"
$env:https_proxy = "http://127.0.0.1:7890"
$env:all_proxy = "http://127.0.0.1:7890"

# NO_PROXY - Domains that bypass proxy
$noProxyList = @(
    "localhost", "127.0.0.1", "::1",
    ".cn",
    ".baidu.com",
    ".aliyuncs.com", ".aliyun.com", ".alibaba.com", ".taobao.com", ".tmall.com",
    ".163.com", ".netease.com",
    ".qq.com", ".tencent.com", ".weixin.qq.com", ".wechat.com",
    ".sina.com.cn", ".weibo.com",
    ".zhihu.com", ".bilibili.com", ".jd.com", ".pinduoduo.com",
    ".meituan.com", ".dianping.com",
    ".bytedance.com", ".toutiao.com", ".douyin.com", ".volces.com", ".ark.cn-beijing.volcesapi.com",
    ".tsinghua.edu.cn", ".edu.cn", ".ac.cn",
    ".xiaomi.com", ".huawei.com"
)
$env:NO_PROXY = $noProxyList -join ","
$env:no_proxy = $env:NO_PROXY

if ($env:HTTP_PROXY -eq "") {
    Write-Host "Proxy Status: OFF"
} else {
    Write-Host "Proxy Status: ON -> $env:HTTP_PROXY"
}