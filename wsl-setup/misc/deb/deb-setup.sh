# checking https://www.notion.so/Windows-Setup-18bd7ba81e6e8018a2c4d6a59f805d01

### ---- debian ----
sudo cp /usr/share/doc/apt/examples/sources.list /etc/apt/sources.list # recover
sudo apt-get update
sudo apt-get install ca-certificates

### configure software source
sudo cat <<'EOF' | sudo tee /etc/apt/sources.list
# Debian 11 (bullseye)
deb [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb [trusted=yes] http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src [trusted=yes] http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src [trusted=yes] http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
EOF

### useful tools 
sudo apt-get update
# vim
sudo apt-get remove vim-common
sudo apt-get install vim
# curl etc
sudo apt install net-tools -y
sudo apt install curl -y
# systemd
sudo apt install -y systemd systemd-sysv dbus
sudo apt install htop -y
# dig and nslookup
sudo apt install dnsutils -y
# podman
sudo apt install podman -y
sudo apt install lsof -y 
sudo apt install sysstat -y

### Others
sudo timedatectl set-timezone Asia/Shanghai
