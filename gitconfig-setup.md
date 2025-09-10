```bash
git config --list --show-origin

git config --global user.name "Dannis"
git config --global user.email hzzhanyuyang@gmail.com

git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"

git config --global alias.cp cherry-pick
git config --global alias.lg "log --abbrev-commit --graph --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %Cblue%an'"
```

# generate ssh key
```bash
# ed25519
ssh-keygen -t ed25519 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/my_ed25519_key -N ""
# RSA
ssh-keygen -m pem -t rsa -b 4096 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/skylab-ec2.pem -N ""
```