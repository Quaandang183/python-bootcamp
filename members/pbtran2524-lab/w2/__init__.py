"""Task Core Management Package.

This package provides essential data structures, file I/O utilities,
and validation logic for task scheduling and workload management.

Exported Symbols:
    - Task: Core dataclass model for task representation.
    - load_tasks: Utility function to parse tasks from CSV/JSON input files.
    - save_json: Utility function to export task data to a JSON file.
    - InfeasiblePlan: Exception raised when workload exceeds capacity.
    - check_feasible: Validator function to check task duration limits.
"""

from .errors import InfeasiblePlan, check_feasible
from .io_utils import load_tasks, save_json
from .models import Task

__all__ = [
    "Task",
    "load_tasks",
    "save_json",
    "InfeasiblePlan",
    "check_feasible",
]