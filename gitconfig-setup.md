```bash
git config --list --show-origin

git config --global user.name "Dannis"
git config --global user.email hzzhanyuyang@gmail.com

git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"
```

# generate ssh key
```bash
# ed25519
ssh-keygen -t ed25519 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/my_ed25519_key -N ""
# RSA
ssh-keygen -m pem -t rsa -b 4096 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/skylab-ec2.pem -N ""
```