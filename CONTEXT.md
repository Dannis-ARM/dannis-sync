# Context

> Domain glossary for dannis-sync

## Terms

### Software
A single software/tool to be installed (e.g., Java, Python, GitHub CLI, PowerShell, etc.). Each Software has zero or more dependencies on other Software.

### Task
A single installation step that executes a script (`.ps1`, `.bat`, or `.cmd`). A Software may consist of one or more Tasks.

### Pre-check
A lightweight check that runs in Python **before** spawning any external processes. Returns `True` if the Software is already installed (skip execution), `False` otherwise. Avoids expensive PowerShell startup overhead for already-installed Software.

### Dependency
A relationship where one Software requires another Software to be installed first.

### Bootstrap
The orchestrator that manages the entire installation flow, respecting dependency order.

### Utils
Independent utility scripts that are deployed to `~/.bin` directory and added to PATH.

### VSCode Sync
(Not to be modified) Module for synchronizing VSCode configurations (`settings.json`, `keybindings.json`) via symbolic links.

