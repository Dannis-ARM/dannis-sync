
set wslDir=%userprofile%\AppData\Local\WSL
mkdir %wslDir%\RHEL10prebuilt
wsl --import RHEL-10-prebuilt %wslDir%\RHEL10prebuilt %wslDir%\rhel-10.0-x86_64-wsl2.tar.gz

wsl --list --verbose

: set default user
wsl RHEL-10-prebuilt config --default-user admin_dannis

: wsl -d RHEL-10-prebuilt

