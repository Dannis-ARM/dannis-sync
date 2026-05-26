"""
Pre-check helper functions for Software installation.

These helpers provide common pre-check patterns that run entirely in Python,
avoiding expensive PowerShell process startup.
"""
import shutil
import subprocess
import logging
from typing import Callable


logger = logging.getLogger(__name__)


def check_command(cmd: str) -> Callable[[], bool]:
    """Check if a command exists in PATH.

    Args:
        cmd: Command name (e.g., "java", "pnpm", "uv")

    Returns:
        Callable that returns True if command exists
    """
    def _check() -> bool:
        found = shutil.which(cmd) is not None
        if found:
            logger.debug(f"✅ Command found: {cmd}")
        return found
    return _check


def check_scoop(package: str) -> Callable[[], bool]:
    """Check if a scoop package is installed.

    Args:
        package: Scoop package name (e.g., "pwsh", "temurin21-jdk")

    Returns:
        Callable that returns True if package is installed
    """
    def _check() -> bool:
        # First check if scoop itself exists
        if shutil.which("scoop") is None:
            return False

        try:
            # Use scoop list --name-only for faster output
            result = subprocess.run(
                ["scoop", "list", "--name-only", package],
                capture_output=True,
                text=True,
                timeout=10
            )
            # If the package is in the output, it's installed
            found = package.lower() in result.stdout.lower()
            if found:
                logger.debug(f"✅ Scoop package found: {package}")
            return found
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            # If anything fails, fall back to installing
            logger.debug(f"⚠️ Scoop check failed for {package}, will run installation")
            return False
    return _check


def run_pre_check(check) -> bool:
    """Run a pre-check (callable or command string).

    Args:
        check: Can be:
            - Callable[[], bool]: Returns True if already installed
            - str: Command to run (exit code 0 = already installed)
            - None: Always returns False (never skip)

    Returns:
        True if already installed (skip), False otherwise
    """
    if check is None:
        return False

    if callable(check):
        try:
            return check()
        except Exception as e:
            logger.debug(f"⚠️ Pre-check callable failed: {e}, will run installation")
            return False

    if isinstance(check, str):
        try:
            result = subprocess.run(
                check,
                shell=True,
                capture_output=True,
                timeout=10
            )
            # Exit code 0 = already installed
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            logger.debug(f"⚠️ Pre-check command failed: {e}, will run installation")
            return False

    # Unknown type, don't skip
    return False
