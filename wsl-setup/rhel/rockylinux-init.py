#!/usr/bin/env python3
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
        capture_output=True,
        text=True,
        errors="ignore"
    )
    if result.returncode != 0:
        return False
    return name in result.stdout.splitlines()


def read_script(filename: str) -> str:
    """Read script content from init directory."""
    script_path = os.path.join(os.path.dirname(__file__), "init", filename)
    with open(script_path, "r", encoding="utf-8") as f:
        return f.read()


def run_wsl_script(distro: str, script_content: str, user: str = "root"):
    """Run a bash script in WSL."""
    cmd = ["wsl", "-d", distro, "-u", user, "bash", "-c", script_content]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Initialize WSL Rocky Linux distro.")
    parser.add_argument("-d", "--distro", default="Rocky-9", help="Distro name (default: Rocky-9)")
    args = parser.parse_args()

    # Check admin
    if not check_admin():
        print("Error: This script requires administrator privileges.", file=sys.stderr)
        sys.exit(1)

    # Check distro exists
    if not distro_exists(args.distro):
        print(f"Error: Distro '{args.distro}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing {args.distro}...")

    # Run setup-clash.sh first
    print("Setting up clash proxy functions...")
    clash_script = read_script("setup-clash.sh")
    run_wsl_script(args.distro, f"""
cat > /tmp/setup-clash.sh << 'EOF'
{clash_script}
EOF
chmod +x /tmp/setup-clash.sh
/tmp/setup-clash.sh
rm -f /tmp/setup-clash.sh
""")

    # Run install-packages.sh
    packages_script = read_script("install-packages.sh")
    run_wsl_script(args.distro, f"""
cat > /tmp/install-packages.sh << 'EOF'
{packages_script}
EOF
clashon
chmod +x /tmp/install-packages.sh
/tmp/install-packages.sh
rm -f /tmp/install-packages.sh
""")

    print("Done!")


if __name__ == "__main__":
    main()
