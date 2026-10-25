"""Core module containing data models, file I/O utilities, and feasibility validation logic.

This module exposes primary domain entities, utility functions for loading/saving data,
and custom exceptions for handling scheduling constraints.
"""

from .models import Task
from .io_utils import load_tasks, save_json
from .errors import InfeasiblePlan, check_feasible

__all__ = ["Task", "load_tasks", "save_json", "InfeasiblePlan", "check_feasible"]