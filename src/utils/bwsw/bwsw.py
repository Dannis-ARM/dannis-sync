import subprocess
import json
import argparse
import sys
import shutil


def check_command(cmd):
    """Check if a command exists on PATH"""
    return shutil.which(cmd) is not None


def get_secrets(project_id=None, search_pattern=None, use_jq=False):
    """Fetch secrets from bws CLI, optionally filter with jq"""
    if not check_command("bws"):
        print("❌ Command not found: bws", file=sys.stderr)
        sys.exit(1)

    cmd = ["bws", "secret", "list", "-o", "json"]
    if project_id:
        cmd.append(project_id)

    try:
        if use_jq and search_pattern:
            if not check_command("jq"):
                print("❌ Command not found: jq", file=sys.stderr)
                sys.exit(1)
            # Use jq for fuzzy filtering
            jq_filter = f'map(select(.key | test("{search_pattern}"; "i")))'
            bws_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
            try:
                jq_proc = subprocess.Popen(["jq", jq_filter], stdin=bws_proc.stdout, stdout=subprocess.PIPE, text=True)
                if bws_proc.stdout:
                    bws_proc.stdout.close()  # Allow bws_proc to receive a SIGPIPE if jq_proc exits
                output, _ = jq_proc.communicate()
                if jq_proc.returncode != 0:
                    print("❌ jq filter failed", file=sys.stderr)
                    sys.exit(1)
                return json.loads(output)
            finally:
                bws_proc.wait()
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fetch secrets: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Failed to parse output", file=sys.stderr)
        sys.exit(1)


def find_secret(secrets, secret_key, fuzzy=False):
    """Find secret by key"""
    if fuzzy:
        # Case-insensitive fuzzy search
        pattern = secret_key.lower()
        matches = [s for s in secrets if pattern in s.get("key", "").lower()]
    else:
        # Exact match
        matches = [s for s in secrets if s.get("key") == secret_key]
    return matches


def handle_get(args):
    """Handle get subcommand"""
    secrets = get_secrets(
        args.project_id,
        search_pattern=args.secret_key if (args.fuzzy and args.jq) else None,
        use_jq=args.jq
    )

    # If jq was used, secrets are already filtered
    if args.jq and args.fuzzy:
        matches = secrets
    else:
        matches = find_secret(secrets, args.secret_key, fuzzy=args.fuzzy)

    if not matches:
        search_type = "fuzzy" if args.fuzzy else "exact"
        print(f"❌ Secret not found ({search_type}): {args.secret_key}", file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1:
        print(f"⚠️ Multiple secrets found with key: {args.secret_key}", file=sys.stderr)
        if args.verbose:
            for i, s in enumerate(matches, 1):
                print(f"  {i}. projectId: {s.get('projectId')}", file=sys.stderr)

    # Output the value of the first match (default behavior for scripting)
    print(matches[0].get("value", ""))

    if args.verbose:
        print(f"\n✅ Found secret: {matches[0].get('key')}", file=sys.stderr)
        print(f"   Project ID: {matches[0].get('projectId')}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Bitwarden Secret Wrapper - Get secrets by key")
    subparsers = parser.add_subparsers(dest="command")

    # Get subcommand
    get_cmd = subparsers.add_parser("get", help="Get secret value by key")
    get_cmd.add_argument("secret_key", help="Secret key to look up")
    get_cmd.add_argument("project_id", nargs="?", help="Optional project ID filter")
    get_cmd.add_argument("-v", "--verbose", action="store_true", help="Show verbose output")
    get_cmd.add_argument("-f", "--fuzzy", action="store_true", help="Enable case-insensitive fuzzy search")
    get_cmd.add_argument("--jq", action="store_true", help="Use jq for filtering (requires jq installed)")

    args = parser.parse_args()

    if args.command == "get":
        handle_get(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
