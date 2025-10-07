# `vscode_config.py` - VSCode Settings Synchronization and Symbolic Link Utility

This command-line utility helps manage VSCode settings synchronization and symbolic links.

## Usage

### Synchronize VSCode Settings

Use the `sync` command to synchronize your VSCode settings between a repository and your local user configuration.

**Actions:**

-   `load-from-repo`: Copies settings from the repository (`configs/settings.json`) to your VSCode user settings (`%HOME%/AppData/Roaming/Code/User/settings.json`).
-   `load-from-vscode`: Copies settings from your VSCode user settings (`%HOME%/AppData/Roaming/Code/User/settings.json`) to the repository (`configs/settings.json`).

**Examples:**

```bash
python vscode_config.py sync load-from-repo   # Copy settings from repo to VSCode
python vscode_config.py sync load-from-vscode # Copy settings from VSCode to repo
```

### Create Symbolic Links

Use the `softlink` command to create symbolic links for files or directories.

**Important Note for Windows Users:**
Please be aware that creating symbolic links on Windows typically requires Administrator privileges.

**Usage:**

-   **Default Symlink for VSCode Settings**: If no arguments are provided, it creates a default symlink where your VSCode user settings file (`%HOME%/AppData/Roaming/Code/User/settings.json`) points to the repository's settings file (`configs/settings.json`).
-   **Custom Symlink**: If `--src` and `--symlink` are provided, it creates a symlink from `--symlink` to `--src`.

**Arguments:**

-   `--src`: The source path (file or directory) to which the symlink should point.
-   `--symlink`: The destination path where the symlink will be created.

**Examples:**

```bash
# Creates a default symlink for VSCode settings:
# (REPO_VSCODE_SETTING_PATH -> VSCODE_SETTING_PATH)
python vscode_config.py softlink

# Creates a custom symlink from C:/path/to/destination to C:/path/to/source
python vscode_config.py softlink --src C:/path/to/source --symlink C:/path/to/destination
