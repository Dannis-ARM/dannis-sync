"""
Script runner utilities.
"""
import subprocess
import logging
import shutil
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)

# Global verbose flag, set by bootstrap.py
_VERBOSE = False


class ScriptRunnerError(Exception):
    """Raised when a script execution fails."""
    pass


class ScriptNotFoundError(ScriptRunnerError):
    """Raised when a script file is not found."""
    pass


def get_pwsh_path() -> str:
    """Get PowerShell executable path, preferring pwsh over powershell.exe."""
    return shutil.which("pwsh") or "powershell.exe"


def run_powershell_script(script_path: Path, capture_output: Optional[bool] = None) -> Optional[str]:
    """Run a PowerShell script with execution policy bypass.

    Args:
        script_path: Path to the .ps1 script file
        capture_output: Whether to capture output (None = auto based on log level)

    Returns:
        Captured output if capture_output is True, else None

    Raises:
        ScriptNotFoundError: If the script file does not exist
        ScriptRunnerError: If the script execution fails
    """
    if not script_path.exists():
        error_msg = f"⚠️ PowerShell script not found: {script_path}"
        logger.warning(error_msg)
        raise ScriptNotFoundError(error_msg)

    # Auto-detect: if not verbose, capture output
    if capture_output is None:
        capture_output = not _VERBOSE

    if logger.getEffectiveLevel() <= logging.INFO:
        logger.info(f"🚀 Running PowerShell script: {script_path.name}")

    try:
        result = subprocess.run(
            [get_pwsh_path(), "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
            check=True,
            capture_output=capture_output,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ PowerShell script failed: {script_path.name}"
        logger.error(error_msg)
        if e.stdout:
            logger.error(f"   Output: {e.stdout}")
        if e.stderr:
            logger.error(f"   Error: {e.stderr}")
        raise ScriptRunnerError(error_msg) from e


def run_batch_script(script_path: Path, capture_output: Optional[bool] = None) -> Optional[str]:
    """Run a Windows batch (.bat/.cmd) script.

    Args:
        script_path: Path to the .bat/.cmd script file
        capture_output: Whether to capture output (None = auto based on log level)

    Returns:
        Captured output if capture_output is True, else None

    Raises:
        ScriptNotFoundError: If the script file does not exist
        ScriptRunnerError: If the script execution fails
    """
    if not script_path.exists():
        error_msg = f"⚠️ Batch script not found: {script_path}"
        logger.warning(error_msg)
        raise ScriptNotFoundError(error_msg)

    # Auto-detect: if not verbose, capture output
    if capture_output is None:
        capture_output = not _VERBOSE

    if logger.getEffectiveLevel() <= logging.INFO:
        logger.info(f"🚀 Running batch script: {script_path.name}")

    try:
        result = subprocess.run(
            ["cmd.exe", "/c", str(script_path)],
            check=True,
            capture_output=capture_output,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Batch script failed: {script_path.name}"
        logger.error(error_msg)
        raise ScriptRunnerError(error_msg) from e


def run_script(script_path: Path, capture_output: Optional[bool] = None) -> Optional[str]:
    """Run a script based on its file extension.

    Args:
        script_path: Path to the script file
        capture_output: Whether to capture output (None = auto based on log level)

    Returns:
        Captured output if capture_output is True, else None

    Raises:
        ScriptNotFoundError: If the script file does not exist
        ScriptRunnerError: If the script execution fails or the file type is unsupported
    """
    suffix = script_path.suffix.lower()

    if suffix == ".ps1":
        return run_powershell_script(script_path, capture_output)
    elif suffix in {".bat", ".cmd"}:
        return run_batch_script(script_path, capture_output)
    else:
        raise ScriptRunnerError(f"Unsupported script type: {suffix}")

