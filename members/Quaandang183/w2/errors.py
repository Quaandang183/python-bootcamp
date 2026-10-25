"""W2-3: feasibility check for a study plan."""

from collections.abc import Iterable

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when the tasks need more hours than are available."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the needed and the available hours."""
        super().__init__(needed_h, available_h)
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self) -> str:
        """Describe how many hours are needed and available."""
        return (
            f"Plan is infeasible: needs {self.needed_h:g}h "
            f"but only {self.available_h:g}h available"
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if the total effort exceeds ``available_h``."""
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
