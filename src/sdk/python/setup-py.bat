

set HTTPS_PROXY=http://127.0.0.1:7890
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

: or if having pipx already
: pipx install uv
