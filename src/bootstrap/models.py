"""
Domain models for the bootstrap system.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional, List, Union


@dataclass
class Task:
    """A single installation task that executes a script."""
    name: str
    script_path: Path
    description: str = ""

    def __post_init__(self):
        if not self.description:
            self.description = f"Install {self.name}"


PreCheck = Union[Callable[[], bool], str, None]


@dataclass
class Software:
    """A software/tool to be installed, consisting of one or more Tasks."""
    name: str
    tasks: List[Task] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Names of other Software
    description: str = ""
    enabled: bool = True
    pre_check: PreCheck = None

    def add_task(self, task: Task) -> "Software":
        self.tasks.append(task)
        return self

    def depends_on(self, *software: "Software") -> "Software":
        self.dependencies.extend(s.name for s in software)
        return self

    def with_pre_check(self, check: PreCheck) -> "Software":
        self.pre_check = check
        return self

