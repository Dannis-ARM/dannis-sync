
import argparse
import logging
import pathlib
import shutil
import sys
import enum

WD = pathlib.Path().resolve()
HOME = pathlib.Path.home()

REPO_VSCODE_SETTING_PATH = WD / "configs" / "settings.json"
VSCODE_SETTING_PATH = HOME / "AppData" / "Roaming" / "Code" / "User" / "settings.json"
VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)

class Action(enum.Enum):
    REPO_LOAD = "load-from-repo"
    VSC_LOAD = "load-from-vscode"
    SOFTLINK_CREATE = "softlink-create"

def create_symlink(to: pathlib.Path, symlink: pathlib.Path):
    """
    Creates a symbolic link 
    Args:
        to (pathlib.Path): The path which the symlink should point.
        symlink (pathlib.Path): The path where the symlink will be created.
    Raises:
        SystemExit: If an exception occurs during symlink creation, the program exits with status 1.
    """
    try:
        if symlink.exists() or symlink.is_symlink():
            symlink.unlink()
        symlink.symlink_to(to)
        logging.info(f"Created symlink: {symlink} -> {to}")
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

    try:
        if args.command == "sync":
            if args.action == Action.REPO_LOAD.value:
                logging.info(f"Copying settings from {REPO_VSCODE_SETTING_PATH} to {VSCODE_SETTING_PATH}")
                shutil.copyfile(REPO_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)
            elif args.action == Action.VSC_LOAD.value:
                logging.info(f"Copying settings from {VSCODE_SETTING_PATH} to {REPO_VSCODE_SETTING_PATH}")
                shutil.copyfile(VSCODE_SETTING_PATH, REPO_VSCODE_SETTING_PATH)
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
