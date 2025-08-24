mkdir -p ~/.cfgs

user_bashrc=~/.cfgs/.bashrc

cat <<'EOF' > ${user_bashrc}

alias ls='ls --color=auto'
alias ll='ls -al'
alias cl='clear'
alias tree='tree -C'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias tmux='tmux -2' # tmux with 256 colors
alias ..='cd ..'

set -o vi
if [ $(id -u) -eq 0 ]; then
        export PS1="\[\e[31m\]\u@\h:\w #\[\e[m\] "
else
        export PS1="\u@\h:\w $ "
fi

EOF

echo '. $user_bashrc' >> ~/.bashrc

