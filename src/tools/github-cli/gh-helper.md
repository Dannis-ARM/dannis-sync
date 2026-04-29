```bat
set REPO_NAME=dannis-authing
set VISIBILITY=public
set GITIGNORE_TPL=Node
set LICENSE_TPL=apache-2.0

gh repo create %REPO_NAME% ^
    --%VISIBILITY% --add-readme ^
    --gitignore %GITIGNORE_TPL% ^
    --license %LICENSE_TPL% ^
    --clone
```