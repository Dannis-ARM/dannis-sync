from utils.install_utils_scripts import PathInstaller
from pathlib import Path
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_powershell_script(script_path: Path) -> None:
    """Run a PowerShell script with execution policy bypass.
    
    Args:
        script_path: Path to the .ps1 script file
    """
    if not script_path.exists():
        logging.warning(f"⚠️ PowerShell script not found: {script_path}")
        return
        
    logging.info(f"🚀 Running PowerShell script: {script_path}")
    try:
        subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
            check=True,
            capture_output=False,
            text=True
        )
        logging.info(f"✅ PowerShell script completed successfully: {script_path.name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ PowerShell script failed: {script_path.name}, error: {e}")

def run_batch_script(script_path: Path) -> None:
    """Run a Windows batch (.bat/.cmd) script.
    
    Args:
        script_path: Path to the .bat/.cmd script file
    """
    if not script_path.exists():
        logging.warning(f"⚠️ Batch script not found: {script_path}")
        return
        
    logging.info(f"🚀 Running batch script: {script_path}")
    try:
        subprocess.run(
            ["cmd.exe", "/c", str(script_path)],
            check=True,
            capture_output=False,
            text=True
        )
        logging.info(f"✅ Batch script completed successfully: {script_path.name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Batch script failed: {script_path.name}, error: {e}")

def run_all_scripts_in_directory(dir_path: Path, recursive: bool = True) -> None:
    """Recursively find and run all .ps1, .bat, .cmd scripts in a directory.
    
    Args:
        dir_path: Path to the directory to search for scripts
        recursive: Whether to search subdirectories recursively, default True
    """
    if not dir_path.exists() or not dir_path.is_dir():
        logging.warning(f"⚠️ Directory not found or not a directory: {dir_path}")
        return
    
    logging.info(f"🔍 Scanning for scripts in directory: {dir_path} (recursive={recursive})")
    
    # Find all script files
    glob_pattern = "**/*" if recursive else "*"
    script_files = sorted([
        f for f in dir_path.glob(glob_pattern)
        if f.is_file() and f.suffix.lower() in {".ps1", ".bat", ".cmd"}
    ])
    
    if not script_files:
        logging.info(f"ℹ️ No scripts found in directory: {dir_path}")
        return
    
    logging.info(f"📦 Found {len(script_files)} scripts to run")
    
    # Run each script by type
    for script in script_files:
        suffix = script.suffix.lower()
        if suffix == ".ps1":
            run_powershell_script(script)
        elif suffix in {".bat", ".cmd"}:
            run_batch_script(script)
    
    logging.info(f"✅ All scripts in directory {dir_path.name} have been processed")

# Run utils installation first
utils_root = Path(__file__).parent.absolute() / "utils"
utils_installer = PathInstaller(str(utils_root))
utils_installer.run()

# Get project root
project_root = Path(__file__).parent.parent.absolute()

# Example 1: Run individual scripts (original approach)
# run_powershell_script(project_root / "src" / "sdk" / "install-choco.ps1")
# run_batch_script(project_root / "src" / "sdk" / "java" / "install.bat")

# Example 2: Run all scripts in sdk directory recursively
# sdk_dir = project_root / "src" / "sdk"
# run_all_scripts_in_directory(sdk_dir)

sdk_dir = project_root / "src" / "pwsh"
run_all_scripts_in_directory(sdk_dir)
