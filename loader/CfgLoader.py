import abc
import pathlib


class CfgLoader(abc.ABC):
    def __init__(self):
        parent_dir = pathlib.Path(__file__).parent.parent
        self.configs_dir = parent_dir / "configs"
        self.user_home = pathlib.Path.home()
        
    @abc.abstractmethod
    def load(self):
        pass

class GitCfgLoader(CfgLoader):
    def __init__(self):
        super().__init__()

    def load(self):
        cfg_file = self.configs_dir / ".gitconfig"

        with open(cfg_file, "r") as f:
            cnt = f.read()
        
        tar_gitconfig_path = self.user_home / ".gitconfig"

        with open(tar_gitconfig_path, "w") as gitconfig_file:
            gitconfig_file.write(cnt)
        print(f".gitconfig file created / updated at {tar_gitconfig_path}")


class BashCfgLoader(CfgLoader):
    def __init__(self):
        super().__init__()

    def load(self):
        src_cfg = self.configs_dir / "unix-configs"/ ".bashrc"

        with open(src_cfg, "r") as f:
            cnt = f.read()
        
        tar_cfg = self.user_home / ".bashrc"

        with open(tar_cfg, "w") as f:
            f.write(cnt)
        print(f".bashrc file created / updated at {tar_cfg}")

class VimCfgLoader(CfgLoader):
    def __init__(self):
        super().__init__()

    def load(self):
        src_cfg = self.configs_dir / "unix-configs"/ ".vimrc"

        with open(src_cfg, "r", encoding='utf-8') as f:
            cnt = f.read()
        
        tar_cfg = self.user_home / ".vimrc"

        with open(tar_cfg, "w", encoding='utf-8') as f:
            f.write(cnt)
        print(f".vimrc file created / updated at {tar_cfg}")

class TmuxCfgLoader(CfgLoader):
    def __init__(self):
        super().__init__()

    def load(self):

        src_cfg = self.configs_dir / "unix-configs"/ ".tmux.conf"

        with open(src_cfg, "r", encoding='utf-8') as f:
            cnt = f.read()
        
        tar_cfg = self.user_home / ".tmux.conf"

        with open(tar_cfg, "w", encoding='utf-8') as f:
            f.write(cnt)
        print(f".tmux.conf file created / updated at {tar_cfg}")

GitCfgLoader().load()
BashCfgLoader().load()
VimCfgLoader().load()
TmuxCfgLoader().load()