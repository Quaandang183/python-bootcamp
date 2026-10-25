"""Workload feasibility validation module.

This module provides custom exceptions and routines to verify if a given set
of scheduled tasks fits within the available execution hours.
"""


class InfeasiblePlan(Exception):
    """Raised when the cumulative duration of tasks exceeds the available working hours."""

    pass


def check_feasible(tasks: list, available_h: float) -> None:
    """Validate whether the total time required for tasks is within available hours.

    Args:
        tasks (list): A list of task objects, where each object has a numeric `duration` attribute.
        available_h (float): Total available working hours.

    Raises:
        InfeasiblePlan: If the sum of all task durations strictly exceeds `available_h`.
    """
    total_hours = sum(task.duration for task in tasks)
    if total_hours > available_h:
        raise InfeasiblePlan(
            f"Kế hoạch không khả thi: Tổng thời gian cần ({total_hours}h) "
            f"vượt quá quỹ thời gian có sẵn ({available_h}h)."
        )