#!/bin/bash

mkdir -p ~/.cfgs

user_bashrc=~/.cfgs/.bashrc

# Write user bashrc (always update to latest version)
cat <<'EOF' > ${user_bashrc}
# Dannis Personal Settings
alias ls='ls --color=auto'
alias ll='ls -alh'
alias cl='clear'
alias tree='tree -C'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
# tmux
alias tmux='tmux -2' # tmux with 256 colors
alias ..='cd ..'
alias ...='cd ./../..'
alias ....='cd ./../../..'
# others

# set PS1
# 跨平台稳健版：绿色用户主机名 + 蓝色路径 + 成功/失败状态提示
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
set -o vi

# Editor setup
# sudo update-alternatives --config editor
EOF

# Source line to add to ~/.bashrc
source_line='user_bashrc=~/.cfgs/.bashrc && . $user_bashrc'

# Check if already in ~/.bashrc (idempotent - only add if not present)
if ! grep -qF "${source_line}" ~/.bashrc 2>/dev/null; then
    echo "${source_line}" >> ~/.bashrc
fi

# Source the config if not already sourced
if [ -z "${BASHRC_SOURCED}" ]; then
    . ~/.bashrc
    export BASHRC_SOURCED=1
fi
