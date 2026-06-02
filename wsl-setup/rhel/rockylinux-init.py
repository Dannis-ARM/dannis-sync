"""Initialize WSL Rocky Linux distro with install-packages.sh and setup-clash.sh."""

import argparse
import os
import subprocess
import sys


def check_admin() -> bool:
    """Check if running as administrator (Windows only)."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        # Non-Windows systems - assume root if uid 0
        return getattr(os, "getuid", lambda: 1000)() == 0


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


def read_script(filename: str) -> str:
    """Read script content from init directory."""
    script_path = os.path.join(os.path.dirname(__file__), "init-scirpts", filename)
    with open(script_path, "r", encoding="utf-8") as f:
        return f.read()


def run_wsl_script(distro: str, script_content: str, user: str = "root"):
    """Run a bash script in WSL via stdin."""
    cmd = ["wsl", "-d", distro, "-u", user, "bash", "-c", "set -euo pipefail; exec bash"]
    result = subprocess.run(cmd, input=script_content.encode("utf-8"))
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Initialize WSL Rocky Linux distro.")
    parser.add_argument("-d", "--distro", default="Rocky-9", help="Distro name (default: Rocky-9)")
    args = parser.parse_args()

    # Check distro exists
    if not distro_exists(args.distro):
        print(f"Error: Distro '{args.distro}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing {args.distro}...")

    # Run setup-clash.sh first
    print("Setting up clash proxy functions...")
    clash_script = read_script("setup-clash.sh")
    run_wsl_script(args.distro, clash_script)

    # Run install-packages.sh
    packages_script = read_script("install-packages.sh")
    run_wsl_script(args.distro, f"""
# Source proxy functions before running
. /usr/local/bin/proxy-functions.sh
clashon || exit 1
{packages_script}
""")

    print("Done!")


if __name__ == "__main__":
    main()
