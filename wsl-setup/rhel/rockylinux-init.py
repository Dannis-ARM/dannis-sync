"""Initialize WSL Rocky Linux distro with wsl.conf, user creation, and init-scripts."""

import argparse
import os
import subprocess
import sys

def distro_exists(name: str) -> bool:
    """Check if WSL distro exists."""
    result = subprocess.run(
        ["wsl", "--list", "--quiet"],
        capture_output=True
    )
    if result.returncode != 0:
        return False
    # Try multiple encodings (utf-16-le is common on Windows)
    for encoding in ["utf-16-le", "utf-8", "gbk"]:
        try:
            stdout = result.stdout.decode(encoding).rstrip("\0")
            if name in stdout.splitlines():
                return True
        except UnicodeDecodeError:
            continue
    return False


def copy_to_wsl(distro: str, src_dir: str, dest: str):
    """Copy a directory from Windows to WSL."""
    # Convert Windows path to WSL path manually: C:\... -> /mnt/c/...
    wsl_src = src_dir.replace("\\", "/")
    if ":" in wsl_src:
        drive, rest = wsl_src.split(":", 1)
        wsl_src = f"/mnt/{drive.lower()}{rest}"

    # Copy in WSL
    subprocess.run(
        ["wsl", "-d", distro, "-u", "root", "bash", "-c",
         f"rm -rf {dest} && mkdir -p $(dirname {dest}) && cp -r {wsl_src} {dest}"],
        check=True
    )


def run_wsl_script(distro: str, script_path: str, user: str = "root", env: dict | None = None):
    """Run a bash script in WSL by path."""
    cmd = ["wsl", "-d", distro, "-u", user, "bash", script_path]
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Initialize WSL Rocky Linux distro.")
    parser.add_argument("-d", "--distro", default="Rocky-9", help="Distro name (default: Rocky-9)")
    parser.add_argument("-u", "--user", default="admin_dannis", help="Default user (default: admin_dannis)")
    args = parser.parse_args()

    # Check distro exists
    if not distro_exists(args.distro):
        print(f"Error: Distro '{args.distro}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing {args.distro}...")

    # Copy init-scripts to WSL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    init_src = os.path.join(script_dir, "init-scirpts")
    init_dest = "/tmp/init-scirpts"
    print(f"Copying {init_src} to {args.distro}:{init_dest}...")
    copy_to_wsl(args.distro, init_src, init_dest)

    # Step 1: Configure wsl.conf (systemd + disable Windows PATH)
    print("Configuring wsl.conf...")
    run_wsl_script(args.distro, f"{init_dest}/configure-wslconf.sh")

    # Step 2: Create default user
    print(f"Creating user {args.user}...")
    env = os.environ.copy()
    env["WSLENV"] = "CREATE_USER"
    env["CREATE_USER"] = args.user
    run_wsl_script(args.distro, f"{init_dest}/create-user.sh", env=env)

    # Step 3: Setup clash proxy functions
    print("Setting up clash proxy functions...")
    run_wsl_script(args.distro, f"{init_dest}/setup-clash.sh")

    # Step 4: Install packages (with proxy enabled)
    print("Installing packages...")
    run_wsl_script(args.distro, f"{init_dest}/install-with-proxy.sh")

    # Step 5: Shutdown to apply wsl.conf changes
    print("Shutting down distro to apply wsl.conf...")
    subprocess.run(["wsl", "-t", args.distro], check=False)
    subprocess.run(["wsl", "--manage", args.distro, "--set-default-user", args.user], check=False)

    print("\nDone!")
    print(f"Use 'wsl -d {args.distro}' to start.")


if __name__ == "__main__":
    main()
