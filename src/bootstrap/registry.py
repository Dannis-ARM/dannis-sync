"""
Registry of all Software available for installation.

This is where you add new Software!
"""
from pathlib import Path
from .models import Software, Task
from .precheck import check_command, check_scoop


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.resolve()


def register_software() -> list[Software]:
    """
    Register all Software and their installation Tasks.

    TO ADD NEW SOFTWARE:
    1. Create your script(s) in the appropriate directory (sdk/, tools/, agents/)
    2. Add a new Software instance below
    3. Add it to the INSTALL_ORDER list

    Returns:
        List of all registered Software
    """
    project_root = get_project_root()
    src_dir = project_root / "src"

    # ------------------------------
    # Core Dependencies (install first)
    # ------------------------------

    scoop = Software(
        name="Scoop",
        description="Windows command-line package manager",
        pre_check=check_command("scoop"),
    ).add_task(Task(
        name="Install Scoop",
        script_path=src_dir / "install-scoop.ps1",
    ))

    # ------------------------------
    # SDKs
    # ------------------------------

    java = Software(
        name="Java",
        description="Java Development Kit",
        pre_check=check_command("java"),
    ).add_task(Task(
        name="Install Java",
        script_path=src_dir / "sdk" / "java" / "install-java.ps1",
    ))

    python_uv = Software(
        name="Python (uv)",
        description="Python with uv package manager",
        pre_check=check_command("uv"),
    ).add_task(Task(
        name="Install uv",
        script_path=src_dir / "sdk" / "python" / "install-uv.bat",
    ))

    node_pnpm = Software(
        name="Node.js (pnpm)",
        description="Node.js with pnpm package manager",
        pre_check=check_command("pnpm"),
    ).add_task(Task(
        name="Install pnpm",
        script_path=src_dir / "sdk" / "node" / "install-pnpm.ps1",
    ))

    node_bun = Software(
        name="Node.js (bun)",
        description="Node.js with Bun runtime",
        pre_check=check_command("bun"),
    ).add_task(Task(
        name="Install Bun",
        script_path=src_dir / "sdk" / "node" / "install-bun.ps1",
    ))

    # ------------------------------
    # Tools
    # ------------------------------

    powershell = Software(
        name="PowerShell",
        description="Latest PowerShell",
        pre_check=check_scoop("pwsh"),
    ).add_task(Task(
        name="Install PowerShell",
        script_path=src_dir / "tools" / "pwsh" / "install-pwsh.ps1",
    ))

    github_cli = Software(
        name="GitHub CLI",
        description="GitHub command-line tool",
        pre_check=check_scoop("gh"),
    ).add_task(Task(
        name="Install GitHub CLI",
        script_path=src_dir / "tools" / "github-cli" / "install-gh.ps1",
    ))

    windows_terminal = Software(
        name="Windows Terminal",
        description="Modern Windows terminal",
        pre_check=check_scoop("windows-terminal"),
    ).add_task(Task(
        name="Install Windows Terminal",
        script_path=src_dir / "tools" / "windows-terminal" / "install-terminal.ps1",
    ))

    # ------------------------------
    # Agents
    # ------------------------------

    claude_cli = Software(
        name="Claude CLI",
        description="Anthropic Claude Code CLI + CC Switch",
        pre_check=check_command("claude"),
    ).add_task(Task(
        name="Install Claude CLI",
        script_path=src_dir / "agents" / "claude" / "install-cc.ps1",
    ))

    claude_skills = Software(
        name="Claude Skills",
        description="Claude Code skills (tdd, grill-with-docs, handoff, etc.)",
        # Skills don't have a simple "installed" check - always run
        # (it's a simple batch script that copies files, idempotent anyway)
    ).depends_on(claude_cli, node_pnpm).add_task(Task(
        name="Setup Skills",
        script_path=src_dir / "agents" / "setup-skills.bat",
    ))
    
    claude_statusline = Software(
        name="Claude Statusline",
        description="Claude Statusline (token usage, model selection)",
    ).depends_on(claude_cli).add_task(Task(
        name="Claude Statusline",
        script_path=src_dir / "agents" / "claude" / "install-cc-statusline.ps1",
    ))

    # ------------------------------
    # Installation Order
    # (Add your new Software here!)
    # ------------------------------

    INSTALL_ORDER = [
        scoop,
        # SDKs
        java,
        python_uv,
        node_pnpm,
        node_bun,
        # Tools
        powershell,
        github_cli,
        windows_terminal,
        # Agents
        claude_cli,
        claude_skills,
        claude_statusline,
    ]

    return INSTALL_ORDER

