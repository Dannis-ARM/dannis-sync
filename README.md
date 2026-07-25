# dannis-sync

> Automated VSCode configuration management and Windows development environment setup tool

## Overview

`dannis-sync` (also known as `vsc-sync`) is a personal development environment automation toolkit designed to streamline the setup and synchronization of development tools, configurations, and SDKs on Windows systems.

## Features

### 🔄 VSCode Configuration Sync
- Creates symbolic links for VSCode `settings.json` and `keybindings.json`
- Automatic backup of existing configurations
- Synchronization between repository and local VSCode user settings
- Located in [src/sync/vsc/vsc-configs/](src/sync/vsc/vsc-configs/)

### 📦 SDK & Tool Installation
Automated installation scripts for:
- **Java** - JDK setup ([src/sdk/java/](src/sdk/java/))
- **Python** - uv package manager ([src/sdk/python/](src/sdk/python/))
- **Node.js** - pnpm & bun ([src/sdk/node/](src/sdk/node/))
- **PowerShell** - Latest PowerShell installation ([src/tools/pwsh/](src/tools/pwsh/))
- **GitHub CLI** - gh command-line tool ([src/tools/github-cli/](src/tools/github-cli/))
- **Windows Terminal** - Modern terminal ([src/tools/windows-terminal/](src/tools/windows-terminal/))
- **Scoop** - Windows package manager ([src/install-scoop.ps1](src/install-scoop.ps1))

### 🤖 Agent & Skill Setup
- Claude Code CLI installation ([src/agents/claude/](src/agents/claude/))
- Skills configuration ([src/agents/setup-skills.bat](src/agents/setup-skills.bat))
- AGENTS.md documentation ([src/agents/AGENTS.md](src/agents/AGENTS.md))

### 🛠️ Utilities
- **Proxy Toggle** - Clash proxy switch scripts ([src/utils/setproxy/](src/utils/setproxy/))
- **Windows Path** - Path management utilities ([src/utils/winpath/](src/utils/winpath/))
- **Windows Startup** - Startup folder management ([src/utils/winstartup/](src/utils/winstartup/))
- **ZIP Hasher** - File integrity checker ([src/utils/hasher_checker/](src/utils/hasher_checker/))
- **Bitwarden Switch** - bwsw utility ([src/utils/bwsw/](src/utils/bwsw/))

### ⚙️ System Configurations
- Git configurations ([configs/git-configs/](configs/git-configs/))
- Unix-style configs (bashrc, tmux, vimrc) ([configs/unix-configs/](configs/unix-configs/))
- Vimium-C config ([configs/vimium-c.conf](configs/vimium-c.conf))

## Getting Started

### Prerequisites
- Python 3.10+
- Windows 10/11
- Git (for repository operations)

### Installation

```powershell
# Clone the repository
git clone <repository-url>
cd dannis-sync

# Set up virtual environment (optional)
python -m venv .venv
.venv\Scripts\Activate

# Install dependencies with uv
uv sync
```

### Usage

#### VSCode Configuration Sync
```powershell
# Create symbolic links for VSCode settings
uv run vsc-sync

# Or create custom symbolic links
uv run vsc-sync --src /path/to/source --symlink /path/to/destination
```

#### Full Environment Bootstrap
```powershell
# Run the Windows bootstrap script (may require Admin privileges)
python src/win-bootstrap.py
```

## Project Structure

```
dannis-sync/
├── configs/              # Configuration files
│   ├── git-configs/     # Git configurations
│   └── unix-configs/    # Unix-style configs
├── src/
│   ├── agents/          # Claude Code agents & skills
│   ├── sdk/             # SDK installation scripts
│   ├── sync/            # Synchronization utilities
│   │   └── vsc/         # VSCode config sync & settings
│   ├── tools/           # Development tools
│   └── utils/           # Helper utilities
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Configuration Files

- **VSCode Settings**: [src/sync/vsc/vsc-configs/settings.json](src/sync/vsc/vsc-configs/settings.json)
- **VSCode Keybindings**: [src/sync/vsc/vsc-configs/keybindings.json](src/sync/vsc/vsc-configs/keybindings.json)

## Development

This project uses **uv** for dependency management and **pytest** for testing.

```powershell
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Dannis - [hzzhanyuyang@gmail.com](mailto:hzzhanyuyang@gmail.com)

