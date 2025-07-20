import pathlib
import shutil
import sys

ACTION = sys.argv[1]

import enum

class Action(enum.Enum):
    REPO_LOAD = "repo-load"
    VSC_LOAD = "vsc-load"

if ACTION not in [LOAD_ACTION.value for LOAD_ACTION in Action]:
    print("Invalid action. Please use 'load' or 'save'.")
    sys.exit(1)

CUR_FILE = pathlib.Path(__file__)
CUR_DIR = CUR_FILE.parent
HOME = pathlib.Path.home()

LOCAL_VSCODE_SETTING_PATH = CUR_DIR / pathlib.Path("configs/settings.json")
VSCODE_SETTING_PATH = HOME / pathlib.Path("AppData/Roaming/Code/User/settings.json")

VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)
if ACTION == Action.REPO_LOAD.value:
    # load_from_repo's setting
    print(f"Copying settings from {LOCAL_VSCODE_SETTING_PATH} to {VSCODE_SETTING_PATH}")
    shutil.copyfile(LOCAL_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)
elif ACTION == Action.VSC_LOAD.value:
    # load from vscode's setting
    print(f"Copying settings from {VSCODE_SETTING_PATH} to {LOCAL_VSCODE_SETTING_PATH}")
    shutil.copyfile(VSCODE_SETTING_PATH, LOCAL_VSCODE_SETTING_PATH)
