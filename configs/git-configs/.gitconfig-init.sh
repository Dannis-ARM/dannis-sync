# git config --global --list
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

### BEGIN [diff enhancements]
# git diff --staged 的别名
git config --global alias.ds "diff --staged"

# git difftool -y 的别名
# 1. 快捷命令：dt = 直接打开图形对比工具（不弹窗确认）
git config --global alias.dt "difftool -y"

# 2. 快捷命令：df = 单词级高亮 diff（最清晰）
git config --global alias.df "diff --color-words"

# 3. diff 颜色主题（超好看）
git config --global diff.color.meta "yellow bold"     # 文件头信息
git config --global diff.color.frag "magenta bold"    # 代码块位置
git config --global diff.color.old "red bold"         # 删除行
git config --global diff.color.new "green bold"        # 新增行
git config --global diff.color.commit "yellow bold"    # 提交信息

# 4. 行内修改精细高亮（比默认强10倍）
git config --global color.diff-highlight.oldNormal "red bold"
git config --global color.diff-highlight.oldHighlight "red bold 52"
git config --global color.diff-highlight.newNormal "green bold"
git config --global color.diff-highlight.newHighlight "green bold 22"

# 5. 终端分页器优化（不闪屏、支持颜色、自动退出）
git config --global core.pager "less -R -F -X -S"
### END

### BEGIN - [diff tools]
git config --global diff.tool vscode
git config --global difftool.vscode.cmd "code --wait --diff \$LOCAL \$REMOTE"
git config --global difftool.prompt false
git config --global alias.dt "difftool -y"
### END

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

git config --global alias.cp cherry-pick
git config --global alias.lg "log --abbrev-commit --graph --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %Cblue%an'"