"""
Main bootstrap entry point.

Sets up the entire Windows development environment:
1. Installs Scoop (package manager)
2. Installs SDKs (Java, Python, Node.js)
3. Installs tools (PowerShell, GitHub CLI, Windows Terminal)
4. Installs Claude Code CLI
5. Deploys utility scripts to ~/.bin

VSCode Sync is in src/sync/vsc/ and NOT modified here.
"""
import argparse
import logging
from pathlib import Path


def setup_logging(verbose: bool):
    """Configure logging based on verbose flag."""
    # Always show INFO for our own logs, only script output capture is controlled by verbose
    level = logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Store verbose flag globally for runner to access
    import bootstrap.runner as runner
    runner._VERBOSE = verbose


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Bootstrap development environment")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all logs")
    args = parser.parse_args()

    setup_logging(args.verbose)

    project_root = Path(__file__).parent.parent.resolve()
    logger.info(f"📍 Project root: {project_root}")
    logger.info("🚀 Starting full bootstrap...\n")

    # ------------------------------
    # Step 1: Install Scoop (core package manager)
    # ------------------------------
    from bootstrap.orchestrator import run_bootstrap
    run_bootstrap()

    # ------------------------------
    # Step 2: Deploy utility scripts
    # ------------------------------
    logger.info("\n" + "="*60)
    logger.info("🔧 Deploying utility scripts")
    logger.info("="*60)

    import sys
    sys.path.insert(0, str(project_root / "src"))
    from utils.install_utils_scripts import PathInstaller

    utils_root = project_root / "src" / "utils"
    installer = PathInstaller(str(utils_root))
    installer.run()

    # ------------------------------
    # Step 3: Sync Agents
    # ------------------------------
    logger.info("\n" + "="*60)
    logger.info("🤖 Syncing agents")
    logger.info("="*60)

    import agents.copy_agents_to_rules as agent
    agent.agent_sync()

    logger.info("\n" + "="*60)
    logger.info("✅ All done!")
    logger.info("="*60)


if __name__ == "__main__":
    main()

