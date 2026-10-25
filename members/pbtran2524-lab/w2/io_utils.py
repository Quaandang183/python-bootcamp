"""Task data model module.

This module defines the core `Task` dataclass used across the application
for task scheduling, priority scoring, and workload management.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represent a scheduled task with effort, priority, and deadline constraints.

    Attributes:
        name (str): The name or brief description of the task.
        duration (float): Estimated time required to complete the task (in hours).
        importance (int): Priority rating level (e.g., scale from 1 to 5).
        deadline (date): The target due date for task completion.
    """

    name: str
    duration: float
    importance: int
    deadline: date

    def days_left(self, today: date) -> int:
        """Calculate the remaining days from a given date until the task's deadline.

        Args:
            today (date): The reference base date used for the calculation.

        Returns:
            int: The non-negative number of days remaining until the deadline.
                Returns 0 if the deadline is today or has already passed.
        """
        remaining_days = (self.deadline - today).days
        return max(0, remaining_days)