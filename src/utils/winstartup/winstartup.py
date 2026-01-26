import logging
import os
import subprocess
import argparse
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def get_startup_folder():
    """
    Retrieve the physical path of the Windows Startup folder for the current user.
    """
    appdata = os.environ.get('APPDATA')
    if not appdata:
        logger.error("Environment variable %APPDATA% not found. Ensure you are on Windows.")
        return None
    return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

def manage_startup_shortcut(action: str, exe_path: str):
    """
    Manage Windows Startup items.
    :param action: 'add' or 'remove'
    :param exe_path: Full path to the target executable
    """
    try:
        # Resolve the absolute path of the EXE
        exe_p = Path(exe_path).resolve()
        startup_folder = get_startup_folder()
        if not startup_folder:
            return

        # Define the shortcut (.lnk) path based on the EXE filename
        shortcut_path = startup_folder / f"{exe_p.stem}.lnk"

        # --- Handle 'remove' action ---
        if action == "remove":
            if shortcut_path.exists():
                shortcut_path.unlink()
                logger.info(f"[-] Successfully removed startup shortcut: {shortcut_path}")
            else:
                logger.warning(f"[!] Shortcut not found, no action needed: {shortcut_path}")
            return

        # --- Handle 'add' action ---
        if action == "add":
            if not exe_p.exists():
                logger.error(f"[X] Target EXE does not exist: {exe_p}")
                return

            # Create startup directory if it's missing
            if not startup_folder.exists():
                logger.info(f"[*] Creating startup directory: {startup_folder}")
                startup_folder.mkdir(parents=True, exist_ok=True)

            # PowerShell command to create a Windows Shortcut via COM
            ps_command = (
                f"$shell = New-Object -ComObject WScript.Shell; "
                f"$shortcut = $shell.CreateShortcut('{str(shortcut_path)}'); "
                f"$shortcut.TargetPath = '{str(exe_p)}'; "
                f"$shortcut.WorkingDirectory = '{str(exe_p.parent)}'; "
                f"$shortcut.Save()"
            )

            # Execute the command
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:
                logger.info(f"[+] Successfully added to startup: {shortcut_path}")
            else:
                logger.error(f"[X] PowerShell failed to create shortcut: {result.stderr}")

    except Exception as e:
        logger.exception(f"[X] An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Windows Startup Manager (shell:startup CLI tool)"
    )
    
    # Mandatory positional arguments
    parser.add_argument(
        "action", 
        choices=["add", "remove"], 
        help="Action to perform: 'add' to create shortcut, 'remove' to delete it."
    )

    parser.add_argument(
        "path", 
        help="Full path to the .exe file."
    )

    args = parser.parse_args()

    # Execution
    manage_startup_shortcut(args.action, args.path)

if __name__ == "__main__":
    main()