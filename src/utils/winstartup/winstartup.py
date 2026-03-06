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
        # 在显示帮助文档时，如果拿不到路径，返回一个提示字符串
        return "Unknown (APPDATA environment variable not found)"
    return str(Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")

def manage_startup_shortcut(action: str, exe_path: str):
    """
    Manage Windows Startup items.
    """
    try:
        exe_p = Path(exe_path).resolve()
        startup_folder_str = get_startup_folder()
        
        if "Unknown" in startup_folder_str:
            logger.error("Could not determine startup folder.")
            return

        startup_folder = Path(startup_folder_str)
        shortcut_path = startup_folder / f"{exe_p.stem}.lnk"

        if action == "remove":
            if shortcut_path.exists():
                shortcut_path.unlink()
                logger.info(f"[-] Successfully removed startup shortcut: {shortcut_path}")
            else:
                logger.warning(f"[!] Shortcut not found, no action needed: {shortcut_path}")
            return

        if action == "add":
            if not exe_p.exists():
                logger.error(f"[X] Target EXE does not exist: {exe_p}")
                return

            if not startup_folder.exists():
                logger.info(f"[*] Creating startup directory: {startup_folder}")
                startup_folder.mkdir(parents=True, exist_ok=True)

            ps_command = (
                f"$shell = New-Object -ComObject WScript.Shell; "
                f"$shortcut = $shell.CreateShortcut('{str(shortcut_path)}'); "
                f"$shortcut.TargetPath = '{str(exe_p)}'; "
                f"$shortcut.WorkingDirectory = '{str(exe_p.parent)}'; "
                f"$shortcut.Save()"
            )

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
    # 获取当前的启动路径
    current_startup_path = get_startup_folder()

    # 在 description 或 epilog 中加入路径信息
    # epilog 会显示在参数说明的最后
    parser = argparse.ArgumentParser(
        description="Windows Startup Manager (shell:startup CLI tool)",
        epilog=f"Current Startup Path: {current_startup_path}",
        formatter_class=argparse.RawDescriptionHelpFormatter # 保持格式输出
    )
    
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
    manage_startup_shortcut(args.action, args.path)

if __name__ == "__main__":
    main()