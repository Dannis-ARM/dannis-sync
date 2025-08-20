
import argparse
import logging
import pathlib
import shutil
import sys
import enum

class Action(enum.Enum):
    REPO_LOAD = "load-from-repo"
    VSC_LOAD = "load-from-vscode"

def main():
    parser = argparse.ArgumentParser(description="Sync VSCode settings between repo and local user config.")
    parser.add_argument(
        "action",
        choices=[action.value for action in Action],
        help="Action to perform: load-from-repo or load-from-vscode"
    )
    args = parser.parse_args()

    CUR_FILE = pathlib.Path(__file__).resolve()
    CUR_DIR = CUR_FILE.parent
    HOME = pathlib.Path.home()

    REPO_VSCODE_SETTING_PATH = CUR_DIR / "configs" / "settings.json"
    VSCODE_SETTING_PATH = HOME / "AppData" / "Roaming" / "Code" / "User" / "settings.json"

    VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        if args.action == Action.REPO_LOAD.value:
            logging.info(f"Copying settings from {REPO_VSCODE_SETTING_PATH} to {VSCODE_SETTING_PATH}")
            shutil.copyfile(REPO_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)
        elif args.action == Action.VSC_LOAD.value:
            logging.info(f"Copying settings from {VSCODE_SETTING_PATH} to {REPO_VSCODE_SETTING_PATH}")
            shutil.copyfile(VSCODE_SETTING_PATH, REPO_VSCODE_SETTING_PATH)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
