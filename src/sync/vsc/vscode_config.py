import argparse
import logging
import pathlib
import shutil
import sys
from datetime import datetime


def find_repo_root(start_path: pathlib.Path) -> pathlib.Path:
    """从当前路径向上查找 git 仓库根目录"""
    current = start_path.resolve()
    while current.parent != current:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise FileNotFoundError("无法找到 git 仓库根目录，请在 git 仓库中运行此脚本")


# 基础路径配置
REPO_ROOT = find_repo_root(pathlib.Path.cwd())
HOME_DIR = pathlib.Path.home()
VSCODE_USER_DIR = HOME_DIR / "AppData" / "Roaming" / "Code" / "User"
REPO_VSCODE_CONFIG_DIR = REPO_ROOT / "configs" / "vsc-configs"
BACKUP_DIR = VSCODE_USER_DIR / "backups"

# VSCode配置文件映射：仓库路径 -> 本地VSCode路径
VSCODE_CONFIG_MAPPING = [
    (REPO_VSCODE_CONFIG_DIR / "settings.json", VSCODE_USER_DIR / "settings.json"),
    (REPO_VSCODE_CONFIG_DIR / "keybindings.json", VSCODE_USER_DIR / "keybindings.json"),
]

# 确保目录存在
VSCODE_USER_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def backup_file(file_path: pathlib.Path) -> None:
    """
    备份文件到备份目录
    :param file_path: 需要备份的文件路径
    """
    if not file_path.exists() or file_path.is_symlink():
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{file_path.stem}_{timestamp}{file_path.suffix}"
    shutil.copy2(file_path, backup_path)
    logging.info(f"💾 已备份原文件: {file_path} -> {backup_path}")


def create_symlink(source: pathlib.Path, symlink_path: pathlib.Path) -> None:
    """
    创建软链接，自动处理目标路径已存在的情况
    :param source: 源文件/目录路径
    :param symlink_path: 软链接路径
    """
    if not source.exists():
        logging.error(f"❌ 源文件不存在: {source}")
        sys.exit(1)

    try:
        # 先备份原文件
        backup_file(symlink_path)

        if symlink_path.is_symlink():
            symlink_path.unlink()
            logging.info(f"🔗 已移除旧软链接: {symlink_path}")
        elif symlink_path.is_dir():
            shutil.rmtree(symlink_path)
            logging.info(f"📂 已移除旧目录: {symlink_path}")
        elif symlink_path.exists():
            symlink_path.unlink()
            logging.info(f"📄 已移除旧文件: {symlink_path}")

        symlink_path.symlink_to(source)
        logging.info(f"✅ 创建软链接成功: {symlink_path} -> {source}")
    except Exception as e:
        logging.error(f"❌ 创建软链接失败: {str(e)}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="📦 VSCode配置软链接创建工具",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--src", type=pathlib.Path, help="源文件/目录路径")
    parser.add_argument("--symlink", type=pathlib.Path, help="软链接目标路径")
    args = parser.parse_args()

    try:
        if args.src and args.symlink:
            create_symlink(args.src.resolve(), args.symlink.resolve())
        else:
            # 默认创建所有VSCode配置软链接
            for src, dst in VSCODE_CONFIG_MAPPING:
                create_symlink(src, dst)
    except Exception as e:
        logging.error(f"❌ 执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
