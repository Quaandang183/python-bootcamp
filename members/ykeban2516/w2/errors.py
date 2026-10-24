from math import isfinite

from .models import Task


class InfeasiblePlan(Exception):
    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(needed_h, available_h)

    def __str__(self) -> str:
        return (
            f"Need {self.needed_h:g} hours, "
            f"but only {self.available_h:g} hours available"
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
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


    