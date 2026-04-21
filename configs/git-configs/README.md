# This is Dannis's Syncing Project

## git tokens
windows
`git config --global credential.helper manager` 
# linux
Token 以明文形式保存在 ~/.git-credentials
`git config --global credential.helper store`

### Fix
https://stackoverflow.com/questions/15589682/how-to-fix-ssh-connect-to-host-github-com-port-22-connection-timed-out-for-g

`edit ~/.ssh/config`
added following
```
Host github.com
 Hostname ssh.github.com
 Port 443
```

```bash
mkdir -p ~/.ssh
cat <<'EOF' > ~/.ssh/config
Host github.com
  Hostname ssh.github.com
  Port 443
EOF
```

ssh -Tv git@github.com