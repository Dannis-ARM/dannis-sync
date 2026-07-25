#!/bin/bash
# ==============================================================
# Git Global Configuration Initialization Script
# ==============================================================
# Check current config: git config --global --list

# ==============================================================
# --- 1. User Profile Settings (global = current user)
# ==============================================================
git config --global user.name          "Dannis"
git config --global user.email         "hzzhanyuyang@gmail.com"

# ==============================================================
# --- 2. Core Default Settings
# ==============================================================
git config --global init.defaultBranch main
git config --global core.pager         "less -R -F -X -S"

# ==============================================================
# --- 3. Git Alias Settings
# ==============================================================
# Basic operation aliases
git config --global alias.st           "status -sb"               # Short status
git config --global alias.co           "checkout"                 # Checkout branch/file
git config --global alias.br           "branch"                   # Branch operations
git config --global alias.mg           "merge"                    # Merge branch
git config --global alias.cm           "commit"                   # Commit changes
git config --global alias.cmm          "commit -m"                # Commit with message
git config --global alias.cp           "cherry-pick"              # Cherry pick commit
git config --global alias.sw           "switch"                   # Switch branch
git config --global alias.rb           "rebase"                   # Rebase branch
git config --global alias.rbi          "rebase -i"                # Interactive rebase
git config --global alias.pr           "pull --rebase"            # Pull with rebase
git config --global alias.last         "log -1 HEAD"              # Show last commit
git config --global alias.mt           "mergetool"                # Open merge tool

# Diff related aliases
git config --global alias.ds           "diff --staged"            # Diff staged changes
git config --global alias.dt           "difftool -y"              # Open diff tool (no prompt)
git config --global alias.df           "diff --color-words"       # Word-level highlighted diff

# Log aliases
git config --global alias.lg           "log --abbrev-commit --graph --pretty=tformat:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %Cblue%an'"
git config --global alias.latest       'for-each-ref --sort=-committerdate --format="%(committername)@%(refname:short) [%(committerdate:short)] %(contents)"'

# ==============================================================
# --- 4. Diff Enhancement Settings
# ==============================================================
# Diff color theme
git config --global diff.color.meta               "yellow bold"    # File header info
git config --global diff.color.frag               "magenta bold"   # Code block position
git config --global diff.color.old                "red bold"       # Deleted lines
git config --global diff.color.new                "green bold"     # Added lines
git config --global diff.color.commit             "yellow bold"    # Commit info

# Inline diff highlight config
git config --global color.diff-highlight.oldNormal    "red bold"
git config --global color.diff-highlight.oldHighlight "red bold 52"
git config --global color.diff-highlight.newNormal    "green bold"
git config --global color.diff-highlight.newHighlight "green bold 22"

# ==============================================================
# --- 5. Diff Tool Settings (VSCode as default)
# ==============================================================
git config --global diff.tool                    vscode
git config --global difftool.vscode.cmd          "code --wait --diff \$LOCAL \$REMOTE"
git config --global difftool.prompt              false
git config --global alias.dt                     "difftool -y"

# ==============================================================
# --- Final Config Verification
# ==============================================================
# Reconfirm user info (redundant but safe)
git config --global user.name          "Dannis"
git config --global user.email         hzzhanyuyang@gmail.com

# Show all configs with origin
git config --list --show-origin