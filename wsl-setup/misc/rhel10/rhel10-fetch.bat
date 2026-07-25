

set wslDir=%userprofile%\AppData\Local\WSL
mkdir %wslDir%
curl -o %wslDir% https://developers.redhat.com/content-gateway/file/rhel/Red_Hat_Enterprise_Linux_10.0/rhel-10.0-x86_64-wsl2.tar.gz

: subscription-manager register to activate redhat individual version
