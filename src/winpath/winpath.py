import winreg
import ctypes
import argparse
from pathlib import Path

# --- Constants ---
REG_ENV_PATH = r"Environment"
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002

class PathManager:
    """Logic class for handling Windows User Environment Variables"""
    
    def __init__(self):
        # Operates on HKEY_CURRENT_USER (User PATH)
        self.hkey = winreg.HKEY_CURRENT_USER

    def _refresh_system(self):
        """Broadcasts a system message to notify that environment variables have changed"""
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
        )

    def get_current_paths(self):
        """Retrieves the current list of paths from the registry"""
        try:
            with winreg.OpenKey(self.hkey, REG_ENV_PATH, 0, winreg.KEY_READ) as key:
                raw_path, _ = winreg.QueryValueEx(key, "PATH")
                return [p.strip() for p in raw_path.split(";") if p.strip()]
        except FileNotFoundError:
            return []

    def save_paths(self, path_list):
        """Writes the path list back to the registry and triggers a system refresh"""
        new_value = ";".join(path_list)
        try:
            with winreg.OpenKey(self.hkey, REG_ENV_PATH, 0, winreg.KEY_WRITE) as key:
                # Use REG_EXPAND_SZ to allow environment variables like %USERPROFILE%
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_value)
            self._refresh_system()
            return True
        except Exception as e:
            print(f"❌ Failed to write to registry: {e}")
            return False

def handle_add(manager, target_paths):
    """Adds new paths to the PATH variable if they don't already exist"""
    current_paths = manager.get_current_paths()
    changed = False
    
    for p in target_paths:
        abs_path = str(Path(p).resolve())
        # Normalization and duplication check
        if any(Path(existing).resolve() == Path(abs_path).resolve() for existing in current_paths):
            print(f"ℹ️ Already exists: {abs_path}")
        else:
            current_paths.append(abs_path)
            print(f"➕ Adding: {abs_path}")
            changed = True

    if changed and manager.save_paths(current_paths):
        print("✅ Batch addition completed.")

def handle_remove(manager, target_paths):
    """Removes specified paths from the PATH variable"""
    current_paths = manager.get_current_paths()
    targets_to_remove = {Path(p).resolve() for p in target_paths}
    
    new_paths = [p for p in current_paths if Path(p).resolve() not in targets_to_remove]
    
    if len(new_paths) < len(current_paths):
        if manager.save_paths(new_paths):
            print(f"🗑️ Successfully removed {len(current_paths) - len(new_paths)} path(s).")
    else:
        print("ℹ️ No matching paths found to remove.")

def handle_clean(manager):
    """Cleans up non-existent paths and removes duplicates"""
    current_paths = manager.get_current_paths()
    seen_paths = set()
    cleaned_paths = []
    
    invalid_count = 0
    duplicate_count = 0

    for p in current_paths:
        path_obj = Path(p)
        # We need to handle potential errors during resolution (e.g., illegal characters)
        try:
            resolved_path = path_obj.resolve()
        except Exception:
            resolved_path = None

        # 1. Check if path exists
        if not path_obj.exists():
            print(f"🧹 Removing invalid path: {p}")
            invalid_count += 1
            continue
        
        # 2. Check for duplicates
        if resolved_path in seen_paths:
            print(f"👯 Removing duplicate path: {p}")
            duplicate_count += 1
            continue
            
        seen_paths.add(resolved_path)
        cleaned_paths.append(p)

    if invalid_count > 0 or duplicate_count > 0:
        if manager.save_paths(cleaned_paths):
            print(f"✨ Cleanup finished: Removed {invalid_count} invalid path(s) and {duplicate_count} duplicate(s).")
    else:
        print("✅ PATH is already clean.")

def main():
    parser = argparse.ArgumentParser(description="Windows User PATH Manager (Enhanced)")
    subparsers = parser.add_subparsers(dest="command")

    # Add subcommand
    add_cmd = subparsers.add_parser("add", help="Add one or more paths")
    add_cmd.add_argument("paths", nargs="+", help="List of paths to add")

    # Remove subcommand
    rm_cmd = subparsers.add_parser("remove", help="Remove one or more paths")
    rm_cmd.add_argument("paths", nargs="+", help="List of paths to remove")

    # Clean subcommand
    subparsers.add_parser("clean", help="Clean invalid paths and duplicates")

    # List subcommand
    subparsers.add_parser("list", help="Display current PATH entries")

    args = parser.parse_args()
    manager = PathManager()

    if args.command == "add":
        handle_add(manager, args.paths)
    elif args.command == "remove":
        handle_remove(manager, args.paths)
    elif args.command == "clean":
        handle_clean(manager)
    elif args.command == "list":
        paths = manager.get_current_paths()
        print("\nCurrent User PATH Variables:")
        for i, p in enumerate(paths, 1):
            status = " [OK]" if Path(p).exists() else " [INVALID!]"
            print(f"  {i:02d}. {p}{status}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()