import logging
import os
import subprocess
import argparse
import sys
from pathlib import Path

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def create_startup_shortcut(exe_path: str):
    """
    Creates a shortcut for the specified exe in the Windows Startup folder.
    Uses native PowerShell to avoid third-party dependencies.
    """
    try:
        # 1. Resolve and validate the executable path
        exe_p = Path(exe_path).resolve()
        if not exe_p.exists():
            logger.error(f"Target EXE does not exist: {exe_p}")
            return

        if exe_p.suffix.lower() != ".exe":
            logger.warning(f"The file '{exe_p.name}' is not an .exe file. Proceeding anyway.")

        # 2. Define the 'shell:startup' physical path
        # Using environment variables to find the user's Roaming AppData
        appdata = os.environ.get('APPDATA')
        if not appdata:
            logger.error("Environment variable %APPDATA% not found.")
            return

        startup_folder = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

        # 3. Create the folder if it doesn't exist (User-custom directory logic)
        if not startup_folder.exists():
            logger.info(f"Directory not found. Creating: {startup_folder}")
            startup_folder.mkdir(parents=True, exist_ok=True)

        # 4. Define the shortcut (.lnk) path
        shortcut_path = startup_folder / f"{exe_p.stem}.lnk"

        # 5. Build PowerShell command
        # We use WScript.Shell via COM to create the shortcut
        ps_command = (
            f"$shell = New-Object -ComObject WScript.Shell; "
            f"$shortcut = $shell.CreateShortcut('{str(shortcut_path)}'); "
            f"$shortcut.TargetPath = '{str(exe_p)}'; "
            f"$shortcut.WorkingDirectory = '{str(exe_p.parent)}'; "
            f"$shortcut.Save()"
        )

        # 6. Execute via subprocess
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode == 0:
            logger.info(f"Successfully created shortcut: {shortcut_path}")
        else:
            logger.error(f"PowerShell failed: {result.stderr}")

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

def main():
    # Initialize argparse for command-line interaction
    parser = argparse.ArgumentParser(
        description="Add an executable to Windows Startup (shell:startup)."
    )
    
    # Add argument for the EXE path
    parser.add_argument(
        "path", 
        help="Full path to the .exe file you want to add to startup."
    )

    args = parser.parse_args()

    # Execute the shortcut creation
    create_startup_shortcut(args.path)

if __name__ == "__main__":
    main()