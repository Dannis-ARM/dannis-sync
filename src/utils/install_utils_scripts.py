from posixpath import sep
import shutil
import platform
import logging
import winreg
import ctypes
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class PathInstaller:
    def __init__(self, source_dir: str, dest_dir: Path = Path.home() / '.bin'):
        self.src = Path(source_dir)
        self.dst = Path(dest_dir)
        self.is_windows = platform.system() == "Windows"

    def _update_windows_path(self):
        """Update Windows User PATH via Registry."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                current_path, _ = winreg.QueryValueEx(key, "Path")
                if str(self.dst) not in current_path:
                    new_path = f"{current_path};{self.dst}" if current_path else str(self.dst)
                    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
                    # Notify system to refresh environment
                    ctypes.windll.user32.SendMessageW(0xFFFF, 0x1A, 0, "Environment")
                    logging.info("Windows PATH updated.")
        except Exception as e:
            logging.error(f"Windows Registry error: {e}")

    def _update_unix_path(self):
        """Update Linux/macOS PATH in shell config files."""
        export_line = f'\nexport PATH="$PATH:{self.dst}"\n'
        configs = [Path.home() / f for f in [".bashrc", ".zshrc", ".profile"]]
        
        for config in filter(lambda p: p.exists(), configs):
            if self.dst.as_posix() not in config.read_text():
                with config.open("a") as f:
                    f.write(export_line)
                logging.info(f"Updated: {config.name}")

    def sync_scripts(self):
        """Flatten and copy scripts, then set permissions."""
        if not self.src.is_dir():
            logging.error(f"Source missing: {self.src}")
            return

        self.dst.mkdir(parents=True, exist_ok=True)

        # Generator for valid files
        scripts = (
            f
            for f in self.src.rglob("*")
            if f.is_file() and f.suffix.lower() in {".py", ".bat"}
        )

        scripts = filter(lambda f: str((f.absolute())) != __file__, scripts)

        count = 0
        for script in scripts:
            target = self.dst / script.name
            shutil.copy2(script, target)
            if not self.is_windows:
                target.chmod(target.stat().st_mode | 0o111)
            count += 1
            logging.info(f"Installed: {script.name}")
        
        logging.info(f"Sync complete. Total: {count}")

    def run(self):
        """Execute installation and PATH update."""
        self.sync_scripts()
        self._update_windows_path() if self.is_windows else self._update_unix_path()

if __name__ == "__main__":
    # Usage
    project_root = Path(__file__).parent.absolute()
    installer = PathInstaller(str(project_root))
    installer.run()