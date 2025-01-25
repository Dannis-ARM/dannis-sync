import pathlib
import shutil
import sys

ACTION = sys.argv[1]

if ACTION not in ["load", "save"]:
    print("Invalid action. Please use 'load' or 'save'.")
    sys.exit(1)

CUR_FILE = pathlib.Path(__file__)
CUR_DIR = CUR_FILE.parent
HOME = pathlib.Path.home()

LOCAL_VSCODE_SETTING_PATH = CUR_DIR / pathlib.Path("configs/settings.json")
VSCODE_SETTING_PATH = HOME / pathlib.Path("AppData/Roaming/Code/User/settings.json")

VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)
if ACTION == "load":
    # load_from_local
    shutil.copyfile(LOCAL_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)
elif ACTION == "save":
    # save_to_local
    shutil.copyfile(VSCODE_SETTING_PATH, LOCAL_VSCODE_SETTING_PATH)