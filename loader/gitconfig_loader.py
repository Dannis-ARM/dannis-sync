import pathlib

def create_gitconfig():
    parent_dir = pathlib.Path(__file__).parent.parent
    configs_dir = parent_dir / "configs"
    src_gitconfig_path = configs_dir / ".gitconfig"

    with open(src_gitconfig_path, "r") as gitconfig_file:
        gitconfig_content = gitconfig_file.read()
    
    tar_gitconfig_path = pathlib.Path.home() / ".gitconfig"

    with open(tar_gitconfig_path, "w") as gitconfig_file:
        gitconfig_file.write(gitconfig_content)
    print(f".gitconfig file created / updated at {tar_gitconfig_path}")

create_gitconfig()