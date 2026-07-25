# Git Configuration

## Credential Helpers

### Windows
Use Windows Credential Manager:
```powershell
git config --global credential.helper manager
```

### Linux
Store credentials in plain text at `~/.git-credentials`:
```bash
git config --global credential.helper store
```

## SSH over HTTPS (Port 443)

Fix "Connection timed out" for GitHub on port 22 by using port 443 instead.

### Quick Setup
```bash
mkdir -p ~/.ssh
cat <<'EOF' > ~/.ssh/config
Host github.com
  Hostname ssh.github.com
  Port 443
EOF
```

### Manual Setup
Edit `~/.ssh/config` and add:
```
Host github.com
  Hostname ssh.github.com
  Port 443
```

### Verify
```bash
ssh -Tv git@github.com
```

## Reference
- [Stack Overflow: Fix SSH connection timeout](https://stackoverflow.com/questions/15589682/how-to-fix-ssh-connect-to-host-github-com-port-22-connection-timed-out-for-g)

