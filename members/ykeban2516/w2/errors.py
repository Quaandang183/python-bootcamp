"""Custom exceptions and plan feasibility validation."""

from math import isfinite

from .models import Task


class InfeasiblePlan(Exception):
    """Exception raised when required task hours exceed available study hours."""

    def __init__(self, needed_h: float, available_h: float):
        """Initialize with required effort and available study hours."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        """Return a formatted error description."""
        return (
            f"Need {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours available"
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Validate whether total task effort fits within available hours.

    Args:
        tasks: List of Task objects to evaluate.
        available_h: Total study time available in hours.

    Raises:
        ValueError: If available_h is not a finite non-negative number.
        InfeasiblePlan: If needed hours strictly exceed available hours.
    """
    if (
        isinstance(available_h, bool)
        or not isinstance(available_h, (int, float))
        or not isfinite(available_h)
        or available_h < 0
    ):
        raise ValueError("available_h must be finite and nonnegative")

    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)



    
