"""
Bootstrap orchestrator - manages the entire installation flow.
"""
import logging
from pathlib import Path
from typing import List, Set

from .models import Software, Task
from .runner import run_script
from .registry import register_software

logger = logging.getLogger(__name__)


class BootstrapOrchestrator:
    """Orchestrates the installation of Software in the correct order."""

    def __init__(self, software_list: List[Software]):
        self.software_list = software_list
        self.installed: Set[str] = set()

    def _can_install(self, software: Software) -> bool:
        """Check if all dependencies of a Software are installed."""
        return all(dep in self.installed for dep in software.dependencies)

    def _install_software(self, software: Software) -> None:
        """Install a single Software by running all its Tasks."""
        if not software.enabled:
            logger.info(f"⏭️ Skipping disabled software: {software.name}")
            return

        for task in software.tasks:
            logger.info(f"🔹 Task: {task.name}")
            run_script(task.script_path)

        self.installed.add(software.name)
        logger.info(f"✅ Completed: {software.name}")

    def run(self) -> None:
        """Run the entire bootstrap process."""
        # Simple linear installation (order respects dependencies)
        for software in self.software_list:
            if not self._can_install(software):
                missing = [dep for dep in software.dependencies if dep not in self.installed]
                logger.warning(f"⚠️ Skipping {software.name} - missing dependencies: {missing}")
                continue

            self._install_software(software)


def run_bootstrap() -> None:
    """Main entry point to run the bootstrap."""
    software_list = register_software()
    orchestrator = BootstrapOrchestrator(software_list)
    orchestrator.run()

