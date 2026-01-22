import socket
import argparse
import sys
import platform

def check_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Check if the service port is open on the specified host.
    Uses high-level create_connection to handle IPv4/IPv6 automatically.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.error, socket.timeout):
        return False

def main():
    parser = argparse.ArgumentParser(description="Detect proxy service and output cross-platform shell commands.")
    parser.add_argument("--host", default="127.0.0.1", help="Proxy host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=7890, help="Proxy port (default: 7890)")
    parser.add_argument("--no-proxy", default="localhost,127.0.0.1,::1", help="Comma-separated domains for NO_PROXY")
    parser.add_argument("--unset", action="store_true", help="Force output of commands to unset proxy variables")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode: only output shell commands")

    args = parser.parse_args()

    # Detect operating system
    is_windows = platform.system() == "Windows"
    
    # Define environment variable lists
    proxy_vars = ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]
    no_proxy_vars = ["NO_PROXY", "no_proxy"]

    def log(msg):
        """Output status messages to stderr to avoid interference with shell eval/parsing"""
        if not args.quiet:
            print(f"# {msg}", file=sys.stderr)

    def output_set(key, value):
        """Format the SET command based on OS"""
        if is_windows:
            print(f"set {key}={value}")
        else:
            print(f'export {key}="{value}"')

    def output_unset(key):
        """Format the UNSET command based on OS"""
        if is_windows:
            print(f"set {key}=")
        else:
            print(f"unset {key}")

    # Logic for unsetting variables
    if args.unset:
        log("Generating commands to unset proxy...")
        for var in proxy_vars + no_proxy_vars:
            output_unset(var)
        return

    # Check service and generate set/unset commands
    log(f"Checking service at {args.host}:{args.port}...")
    if check_port(args.host, args.port):
        proxy_url = f"http://{args.host}:{args.port}"
        log("Service is UP. Generating set commands.")
        for var in proxy_vars:
            output_set(var, proxy_url)
        for var in no_proxy_vars:
            output_set(var, args.no_proxy)
    else:
        log("Service is DOWN. Generating unset commands.")
        for var in proxy_vars + no_proxy_vars:
            output_unset(var)

if __name__ == "__main__":
    main()