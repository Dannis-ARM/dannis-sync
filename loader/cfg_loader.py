"""
This script handles the loading of configuration files from the project's 'configs'
directory to the user's home directory, making it easy to synchronize settings.
"""

import abc
import pathlib
import shutil


class CfgLoader(abc.ABC):
    """
    Abstract base class for configuration loaders.

    It provides a standardized way to copy configuration files from a source
    location within the project to a destination in the user's home directory.

    Subclasses must define the `src_rel_path` and `dest_filename` class attributes.
    """

    # Relative path to the source file from the project root.
    src_rel_path: str = ""
    # Name of the destination file in the user's home directory.
    dest_filename: str = ""

    def __init__(self):
        """Initializes the loader by resolving source and destination paths."""
        if not self.src_rel_path or not self.dest_filename:
            raise NotImplementedError(
                "Subclasses must define src_rel_path and dest_filename."
            )

        project_root = pathlib.Path(__file__).parent.parent
        self.user_home = pathlib.Path.home()
        self.src_path = project_root / self.src_rel_path
        self.dest_path = self.user_home / self.dest_filename

    def load(self):
        """
        Copies the configuration file from the source to the destination.
        If the destination file already exists, it will be overwritten.
        """
        try:
            # Ensure the parent directory of the destination file exists.
            self.dest_path.parent.mkdir(parents=True, exist_ok=True)
            # Use shutil.copy for a robust file copy operation.
            shutil.copy(self.src_path, self.dest_path)
            print(f"Successfully loaded '{self.src_path.name}' to '{self.dest_path}'")
        except FileNotFoundError:
            print(f"Error: Source file not found at '{self.src_path}'")
        except Exception as e:
            print(f"An error occurred while loading '{self.src_path.name}': {e}")


class GitCfgLoader(CfgLoader):
    """Loads the .gitconfig file."""

    src_rel_path = "configs/.gitconfig"
    dest_filename = ".gitconfig"


class BashCfgLoader(CfgLoader):
    """Loads the .bashrc file."""

    src_rel_path = "configs/unix-configs/.bashrc"
    dest_filename = ".bashrc"


class VimCfgLoader(CfgLoader):
    """Loads the .vimrc file."""

    src_rel_path = "configs/unix-configs/.vimrc"
    dest_filename = ".vimrc"


class TmuxCfgLoader(CfgLoader):
    """Loads the .tmux.conf file."""

    src_rel_path = "configs/unix-configs/.tmux.conf"
    dest_filename = ".tmux.conf"


def main():
    """
    Initializes and runs all configuration loaders.

    This function serves as the main entry point for the script.
    """

    print("Starting configuration loading process...")

    loaders = [
        GitCfgLoader,
        BashCfgLoader,
        VimCfgLoader,
        TmuxCfgLoader,
    ]

    for loader_class in loaders:
        loader_instance = loader_class()

        loader_instance.load()

    print("Configuration loading process finished.")


# Run the main function to load all configurations when the script is executed.


main()
