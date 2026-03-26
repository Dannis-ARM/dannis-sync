
import argparse
import logging
import pathlib
import shutil
import sys
import enum

FILE_WD = pathlib.Path(__file__).resolve().parent.parent.parent.parent

logging.info(f"FILE_WD: {FILE_WD}")
HOME = pathlib.Path.home()

# settings.json paths
REPO_VSCODE_SETTING_PATH = FILE_WD / "configs" / "settings.json"
VSCODE_SETTING_PATH = HOME / "AppData" / "Roaming" / "Code" / "User" / "settings.json"

# keybindings.json paths
REPO_VSCODE_KEYBINDINGS_PATH = FILE_WD / "configs" / "keybindings.json"
VSCODE_KEYBINDINGS_PATH = HOME / "AppData" / "Roaming" / "Code" / "User" / "keybindings.json"

# Ensure VSCode User directory exists
VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)

class Action(enum.Enum):
    REPO_LOAD = "load-from-repo"
    VSC_LOAD = "load-from-vscode"
    SOFTLINK_CREATE = "softlink-create"

def create_symlink(point_to: pathlib.Path, symlink: pathlib.Path):
    """
    Creates a symbolic link. If a file, directory, or another symlink already exists
    at the destination, it will be removed before the new symlink is created.
    Args:
        to (pathlib.Path): The path to which the symlink should point.
        symlink (pathlib.Path): The path where the symlink will be created.
    Raises:
        SystemExit: If an exception occurs during the process, the program exits with status 1.
    """
    try:
        # The is_symlink() check must come first, as a symlink to a directory
        # will also return True for is_dir().
        if symlink.is_symlink():
            symlink.unlink()
            logging.info(f"Removed existing symlink: {symlink}")
        elif symlink.is_dir():
            shutil.rmtree(symlink)
            logging.info(f"Removed existing directory: {symlink}")
        elif symlink.exists():
            symlink.unlink()
            logging.info(f"Removed existing file: {symlink}")

        symlink.symlink_to(point_to)
        logging.info(f"Created symlink: {symlink} -> {point_to}")
    except Exception as e:
        logging.error(f"Failed to create symlink: {e}")
        sys.exit(1)

def cli():
    parser = argparse.ArgumentParser(
        description="""
        A command-line utility to manage VSCode settings synchronization and symbolic links.

        Use 'sync' to synchronize your VSCode settings between a repository and your local user configuration.
        Use 'softlink' to create symbolic links for files or directories.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for sync actions
    sync_parser = subparsers.add_parser(
        "sync",
        help="""
        Synchronize VSCode settings.

        Examples:
          python vscode_config.py sync load-from-repo   # Copy settings from repo to VSCode
          python vscode_config.py sync load-from-vscode # Copy settings from VSCode to repo
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    sync_parser.add_argument(
        "action",
        choices=[Action.REPO_LOAD.value, Action.VSC_LOAD.value],
        help="""
        Action to perform:
          load-from-repo: Copies settings from the repository to your VSCode user settings.
          load-from-vscode: Copies settings from your VSCode user settings to the repository.
        """
    )

    # Subparser for softlink creation
    softlink_parser = subparsers.add_parser(
        "softlink",
        help="""
        Create a symbolic link.

        If --src and --symlink are provided, creates a symlink from --symlink to --src.
        If no arguments are provided, creates a default symlink for VSCode settings:
        (REPO_VSCODE_SETTING_PATH -> VSCODE_SETTING_PATH)

        Examples: (Please be aware you need to be Admin on Windows)
          python vscode_config.py softlink --src C:/path/to/source --symlink C:/path/to/destination
          python vscode_config.py softlink # Creates default symlink for VSCode settings 
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    softlink_parser.add_argument(
        "--src",
        type=pathlib.Path,
        required=False,
        help="The source path (file or directory) to which the symlink should point."
    )
    softlink_parser.add_argument(
        "--symlink",
        type=pathlib.Path,
        required=False,
        help="The destination path where the symlink will be created."
    )

    args = parser.parse_args()

    def sync_file(src: pathlib.Path, dst: pathlib.Path, file_desc: str):
        """Sync a single file, handling missing files and symlinks gracefully."""
        # Resolve symlinks to handle the case where src and dst are the same file
        src_resolved = src.resolve() if src.exists() else None
        dst_resolved = dst.resolve() if dst.exists() else None
        
        # Skip if both files exist and are the same (e.g., symlink case)
        if src_resolved and dst_resolved and src_resolved == dst_resolved:
            logging.info(f"Skipped {file_desc}: source and destination are the same file")
            return
            
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            logging.info(f"Copied {file_desc} from {src} to {dst}")
        else:
            logging.warning(f"Source {file_desc} not found: {src}")

    try:
        if args.command == "sync":
            if args.action == Action.REPO_LOAD.value:
                # Copy settings.json
                sync_file(REPO_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH, "settings.json")
                # Copy keybindings.json
                sync_file(REPO_VSCODE_KEYBINDINGS_PATH, VSCODE_KEYBINDINGS_PATH, "keybindings.json")
            elif args.action == Action.VSC_LOAD.value:
                # Copy settings.json
                sync_file(VSCODE_SETTING_PATH, REPO_VSCODE_SETTING_PATH, "settings.json")
                # Copy keybindings.json
                sync_file(VSCODE_KEYBINDINGS_PATH, REPO_VSCODE_KEYBINDINGS_PATH, "keybindings.json")
        elif args.command == "softlink":
            if args.src is None or args.symlink is None:
                create_symlink(REPO_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)
            else:
                create_symlink(args.src, args.symlink)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

def main():
    cli()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
