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

### Proxy Configuration
Shadowrocket or similar proxy rule configuration files that define routing policies for network traffic.

### Stocks Broker
Securities trading platforms. The project maintains proxy routing rules for:
- **IBKR** (Interactive Brokers): routes DIRECT
- **Schwab** (Charles Schwab): routes DIRECT
- **Firstrade**: routes via 美国硅谷 (US Silicon Valley proxy)

### DIRECT
Proxy policy meaning traffic connects directly without going through any proxy.

### 美国硅谷 (US Silicon Valley)
A specific proxy group/node in the proxy configuration for routing traffic through Silicon Valley, USA.

