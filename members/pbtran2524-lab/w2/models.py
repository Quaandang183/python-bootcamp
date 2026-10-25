"""Task data model module.

This module defines the core `Task` dataclass used for task management,
priority scoring, and scheduling calculations.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represent an individual task with scheduling constraints and importance.

    Attributes:
        name (str): The name or brief title of the task.
        duration (float): Estimated effort or time required to complete the task (in hours).
        importance (int): Numerical importance rating (e.g., scale from 1 to 5).
        deadline (date): Target completion date for the task.
    """

    name: str
    duration: float
    importance: int
    deadline: date

    def days_left(self, today: date) -> int:
        """Calculate the remaining days from a given date until the task's deadline.

        Args:
            today (date): The reference date to calculate remaining days from.

        Returns:
            int: The non-negative number of days remaining until the deadline.
                Returns 0 if the deadline has already passed or is today.
        """
        remaining_days = (self.deadline - today).days
        return max(0, remaining_days)