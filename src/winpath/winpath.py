import winreg
import ctypes
import argparse
from pathlib import Path

# --- 常量定义 ---
REG_ENV_PATH = r"Environment"
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002

class PathManager:
    """处理 Windows 用户环境变量的逻辑类"""
    
    def __init__(self):
        self.hkey = winreg.HKEY_CURRENT_USER

    def _refresh_system(self):
        """发送系统广播，通知环境变量已更改"""
        result = ctypes.c_long()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
        )

    def get_current_paths(self):
        """获取当前所有的路径列表"""
        try:
            with winreg.OpenKey(self.hkey, REG_ENV_PATH, 0, winreg.KEY_READ) as key:
                raw_path, _ = winreg.QueryValueEx(key, "PATH")
                return [p.strip() for p in raw_path.split(";") if p.strip()]
        except FileNotFoundError:
            return []

    def save_paths(self, path_list):
        """将路径列表写回注册表并广播"""
        new_value = ";".join(path_list)
        try:
            with winreg.OpenKey(self.hkey, REG_ENV_PATH, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_value)
            self._refresh_system()
            return True
        except Exception as e:
            print(f"❌ 写入注册表失败: {e}")
            return False

def handle_add(manager, target_paths):
    current_paths = manager.get_current_paths()
    changed = False
    
    for p in target_paths:
        abs_path = str(Path(p).resolve())
        # 规范化去重
        if any(Path(existing).resolve() == Path(abs_path).resolve() for existing in current_paths):
            print(f"ℹ️ 已存在: {abs_path}")
        else:
            current_paths.append(abs_path)
            print(f"➕ 添加: {abs_path}")
            changed = True

    if changed and manager.save_paths(current_paths):
        print("✅ 批量添加完成。")

def handle_remove(manager, target_paths):
    current_paths = manager.get_current_paths()
    targets_to_remove = {Path(p).resolve() for p in target_paths}
    
    new_paths = [p for p in current_paths if Path(p).resolve() not in targets_to_remove]
    
    if len(new_paths) < len(current_paths):
        if manager.save_paths(new_paths):
            print(f"🗑️ 成功移除了 {len(current_paths) - len(new_paths)} 个路径。")
    else:
        print("ℹ️ 未发现匹配的可移除路径。")

def handle_clean(manager):
    """清理不存在的路径以及重复的路径"""
    current_paths = manager.get_current_paths()
    seen_paths = set()
    cleaned_paths = []
    
    invalid_count = 0
    duplicate_count = 0

    for p in current_paths:
        path_obj = Path(p)
        resolved_path = path_obj.resolve()

        # 1. 检查是否存在
        if not path_obj.exists():
            print(f"🧹 移除失效路径: {p}")
            invalid_count += 1
            continue
        
        # 2. 检查是否重复
        if resolved_path in seen_paths:
            print(f"👯 移除重复路径: {p}")
            duplicate_count += 1
            continue
            
        seen_paths.add(resolved_path)
        cleaned_paths.append(p)

    if invalid_count > 0 or duplicate_count > 0:
        if manager.save_paths(cleaned_paths):
            print(f"✨ 清理完毕：移除了 {invalid_count} 个失效路径，{duplicate_count} 个重复路径。")
    else:
        print("✅ PATH 非常干净，无需清理。")

def main():
    parser = argparse.ArgumentParser(description="Windows 用户 PATH 管理增强版")
    subparsers = parser.add_subparsers(dest="command")

    # Add 子命令
    add_cmd = subparsers.add_parser("add", help="添加一个或多个路径")
    add_cmd.add_argument("paths", nargs="+", help="路径列表")

    # Remove 子命令
    rm_cmd = subparsers.add_parser("remove", help="移除一个或多个路径")
    rm_cmd.add_argument("paths", nargs="+", help="路径列表")

    # Clean 子命令
    subparsers.add_parser("clean", help="清理不存在的路径及重复项")

    # List 子命令
    subparsers.add_parser("list", help="显示当前 PATH")

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
        print("\n当前用户 PATH 变量:")
        for i, p in enumerate(paths, 1):
            status = " [OK]" if Path(p).exists() else " [INVALID!]"
            print(f"  {i:02d}. {p}{status}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()