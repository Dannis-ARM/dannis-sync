# enable proxy (optional)
# export HTTPS_PROXY=http://192.168.31.15:7890

# curl
sudo dnf install curl -y
# network tools 
sudo dnf install bind-utils -y
# podman
sudo dnf install podman -y
sudo dnf install podman-docker -y
# vim
sudo dnf install vim -y
# for clear cmd
sudo dnf install ncurses -y
# for git
sudo dnf install git -y
sudo dnf install unzip

### EPEL (Extra Packages for Enterprise Linux) 仓库。
# https://docs.fedoraproject.org/en-US/epel/getting-started/
sudo subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm -y
sudo dnf install htop -y