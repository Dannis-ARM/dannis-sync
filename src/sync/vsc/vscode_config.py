import argparse
import logging
import pathlib
import shutil
import sys

# 基础路径配置
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
HOME_DIR = pathlib.Path.home()
VSCODE_USER_DIR = HOME_DIR / "AppData" / "Roaming" / "Code" / "User"
REPO_VSCODE_CONFIG_DIR = ROOT_DIR / "configs" / "vsc-configs"

# VSCode配置文件映射：仓库路径 -> 本地VSCode路径
VSCODE_CONFIG_MAPPING = [
    (REPO_VSCODE_CONFIG_DIR / "settings.json", VSCODE_USER_DIR / "settings.json"),
    (REPO_VSCODE_CONFIG_DIR / "keybindings.json", VSCODE_USER_DIR / "keybindings.json"),
]

# 确保目录存在
VSCODE_USER_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_symlink(source: pathlib.Path, symlink_path: pathlib.Path) -> None:
    """
    创建软链接，自动处理目标路径已存在的情况
    :param source: 源文件/目录路径
    :param symlink_path: 软链接路径
    """
    try:
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
            create_symlink(args.src, args.symlink)
        else:
            # 默认创建所有VSCode配置软链接
            for src, dst in VSCODE_CONFIG_MAPPING:
                create_symlink(src, dst)
    except Exception as e:
        logging.error(f"❌ 执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()