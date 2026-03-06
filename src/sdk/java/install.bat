scoop config proxy 127.0.0.1:7890

: aria2
scoop install aria2
scoop config aria2-enabled true
scoop config aria2-max-connection-per-server 16
scoop config aria2-split 5

scoop bucket add java

scoop install temurin8-jdk
scoop install temurin21-jdk