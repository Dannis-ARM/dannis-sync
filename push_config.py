import pathlib
import shutil

CUR_FILE = pathlib.Path(__file__)
CUR_DIR = CUR_FILE.parent
HOME = pathlib.Path.home()

LOCAL_VSCODE_SETTING_PATH = CUR_DIR / pathlib.Path("configs/settings.json")
VSCODE_SETTING_PATH = HOME / pathlib.Path("AppData/Roaming/Code/User/settings.json")

VSCODE_SETTING_PATH.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(LOCAL_VSCODE_SETTING_PATH, VSCODE_SETTING_PATH)