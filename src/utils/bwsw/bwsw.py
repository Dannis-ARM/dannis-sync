import subprocess
import json
import argparse
import sys


def get_secrets(project_id=None):
    """Fetch secrets from bws CLI"""
    cmd = ["bws", "secret", "list", "-o", "json"]
    if project_id:
        cmd.append(project_id)

    try:
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
        print(f"❌ Failed to parse bws output", file=sys.stderr)
        sys.exit(1)


def find_secret(secrets, secret_key):
    """Find secret by key (case-sensitive exact match)"""
    matches = [s for s in secrets if s.get("key") == secret_key]
    return matches


def handle_get(args):
    """Handle get subcommand"""
    secrets = get_secrets(args.project_id)
    matches = find_secret(secrets, args.secret_key)

    if not matches:
        print(f"❌ Secret not found: {args.secret_key}", file=sys.stderr)
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

    args = parser.parse_args()

    if args.command == "get":
        handle_get(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
