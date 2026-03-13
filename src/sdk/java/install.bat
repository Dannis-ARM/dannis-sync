setproxy
scoop config proxy 127.0.0.1:7890

: aria2
scoop install aria2
scoop config aria2-enabled true
scoop config aria2-max-connection-per-server 16
scoop config aria2-split 32
scoop config aria2-min-split-size 1M
scoop config aria2-retry-wait 4

scoop bucket add java

scoop install temurin8-jdk
scoop install temurin21-jdk

: switch jdk versions
: scoop reset temurin8-jdk
: scoop reset temurin21-jdk
