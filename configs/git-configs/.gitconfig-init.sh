# --- profile settings ---
# (--global means current user)
git config --global user.name "Dannis"
git config --global user.email "hzzhanyuyang@gmail.com"

# --- alias settings ---
git config --global init.defaultBranch main

# git status -sb 的别名
git config --global alias.st "status -sb"

# git checkout 的别名
git config --global alias.co "checkout"

# git branch 的别名
git config --global alias.br "branch"

# git merge 的别名
git config --global alias.mg "merge"

# git commit 的别名
git config --global alias.cm "commit"

# git commit -m 的别名
git config --global alias.cmm "commit -m"

# git diff --staged 的别名
git config --global alias.ds "diff --staged"

# git difftool -y 的别名
git config --global alias.dt "difftool -y"

# git mergetool 的别名
git config --global alias.mt "mergetool"

# git log -1 HEAD 的别名
git config --global alias.last "log -1 HEAD"

# git for-each-ref --sort=-committerdate --format="..." 的别名 (这个命令比较长，确保引号完整)
git config --global alias.latest 'for-each-ref --sort=-committerdate --format="%(committername)@%(refname:short) [%(committerdate:short)] %(contents)"'

# git pull --rebase 的别名
git config --global alias.pr "pull --rebase"

# git switch 的别名
git config --global alias.sw "switch"

# git rebase 的别名
git config --global alias.rb "rebase"

# git rebase -i 的别名
git config --global alias.rbi "rebase -i"

git config --list --show-origin

git config --global user.name "Dannis"
git config --global user.email hzzhanyuyang@gmail.com

git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"

git config --global alias.cp cherry-pick
git config --global alias.lg "log --abbrev-commit --graph --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %Cblue%an'"