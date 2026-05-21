@echo off
:: clashon.bat - Turn on proxy using Clash
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
set ALL_PROXY=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set https_proxy=http://127.0.0.1:7890
set all_proxy=http://127.0.0.1:7890

:: NO_PROXY - Domains that bypass proxy
set NO_PROXY_LIST=localhost,127.0.0.1,::1
set NO_PROXY_LIST=%NO_PROXY_LIST%,.cn
set NO_PROXY_LIST=%NO_PROXY_LIST%,.baidu.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.aliyuncs.com,.aliyun.com,.alibaba.com,.taobao.com,.tmall.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.163.com,.netease.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.qq.com,.tencent.com,.weixin.qq.com,.wechat.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.sina.com.cn,.weibo.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.zhihu.com,.bilibili.com,.jd.com,.pinduoduo.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.meituan.com,.dianping.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.bytedance.com,.toutiao.com,.douyin.com,.volces.com,.ark.cn-beijing.volcesapi.com
set NO_PROXY_LIST=%NO_PROXY_LIST%,.tsinghua.edu.cn,.edu.cn,.ac.cn
set NO_PROXY_LIST=%NO_PROXY_LIST%,.xiaomi.com,.huawei.com

set NO_PROXY=%NO_PROXY_LIST%
set no_proxy=%NO_PROXY_LIST%

if "%HTTP_PROXY%"=="" (
    echo Proxy Status: OFF
) else (
    echo Proxy Status: ON -^> %HTTP_PROXY%
)