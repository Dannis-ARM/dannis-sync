#!/bin/sh
cur=$(pwd)

cd ~

bashrc=https://raw.githubusercontent.com/Dannis-ARM/dannis-sync/refs/heads/main/configs/unix-configs/.bashrc-init.sh
curl -O $bashrc
sh .bashrc-init.sh
rm .bashrc-init.sh

vimrc=https://raw.githubusercontent.com/Dannis-ARM/dannis-sync/refs/heads/main/configs/unix-configs/.vimrc-init.sh
curl -O $vimrc
sh .vimrc-init.sh
rm .vimrc-init.sh

cd $cur