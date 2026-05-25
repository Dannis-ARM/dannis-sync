# Adding New Tools

This guide explains how to add new software/tools to the bootstrap process.

## Quick Start

### Step 1: Add your installation script

Create your script in the appropriate directory:
- `src/sdk/<your-tool>/` - For SDKs (Java, Python, Node.js, etc.)
- `src/tools/<your-tool>/` - For tools (PowerShell, GitHub CLI, etc.)
- `src/agents/<your-tool>/` - For agents/CLI tools

Example:
```
src/tools/my-new-tool/
└── install-my-new-tool.ps1
```

### Step 2: Register the Software

Edit `src/bootstrap/registry.py`:

```python
# 1. Define your Software somewhere in the file
my_new_tool = Software(
    name="My New Tool",
    description="What it does",
).add_task(Task(
    name="Install My New Tool",
    script_path=src_dir / "tools" / "my-new-tool" / "install-my-new-tool.ps1",
))

# 2. Add it to the INSTALL_ORDER list at the end
INSTALL_ORDER = [
    # ... existing tools ...
    my_new_tool,  # <-- Add this line
]
```

### Step 3: You're done!

Run the bootstrap:
```powershell
python src/bootstrap.py
```

## Dependency Management

If your tool depends on another tool being installed first:

```python
my_new_tool = Software(
    name="My New Tool",
    description="Depends on Scoop",
).depends_on("Scoop")  # <-- Add this line
 .add_task(Task(...))
```

## Multiple Tasks

A single Software can have multiple installation tasks:

```python
my_new_tool = Software(
    name="My New Tool",
    description="Multi-step install",
).add_task(Task(
    name="Step 1: Install base",
    script_path=src_dir / "tools" / "my-new-tool" / "step1.ps1",
)).add_task(Task(
    name="Step 2: Configure",
    script_path=src_dir / "tools" / "my-new-tool" / "step2.ps1",
))
```

