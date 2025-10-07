# This is Dannis's Syncing Project

### git clone
```cmd
git remote remove origin 
git remote add origin git@github.com:Dannis-ARM/dannis-sync.git

```

### Fix
https://stackoverflow.com/questions/15589682/how-to-fix-ssh-connect-to-host-github-com-port-22-connection-timed-out-for-g

`edit ~/.ssh/config`
added following
```
Host github.com
 Hostname ssh.github.com
 Port 443
```