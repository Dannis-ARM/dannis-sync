import pathlib

from src.sync.vsc.vscode_config import create_symlink
WD = pathlib.Path().resolve()

def test_create_symlink():
    create_symlink(WD / 'README.md', WD / 'README-TAR.md')

