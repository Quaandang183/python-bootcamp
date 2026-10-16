from datetime import date

from shared.contract import Task


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    """Sort tasks by decreasing priority, preserving ties."""
    return sorted(
        tasks,
        key=lambda task: task.importance / max(
            (task.deadline - today).days, 1
        ),
        reverse=True,
    )
