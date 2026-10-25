"""Data models for scheduled study tasks."""

from dataclasses import dataclass
from datetime import date
from math import isfinite


@dataclass
class Task:
    """Represents a scheduled study task with priority, effort, and deadline.

    Attributes:
        title: Descriptive name of the task.
        importance: Integer priority level from 1 (low) to 5 (high).
        effort_h: Required duration in hours (finite and nonnegative).
        deadline: Due date for completing the task.
    """

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
        """Validate task fields after dataclass initialization."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must not be empty")

        if type(self.importance) is not int or not 1 <= self.importance <= 5:
            raise ValueError("importance must be an integer from 1 to 5")

        if (
            isinstance(self.effort_h, bool)
            or not isinstance(self.effort_h, (int, float))
            or not isfinite(self.effort_h)
            or self.effort_h < 0
        ):
            raise ValueError("effort_h must be finite and nonnegative")

        if type(self.deadline) is not date:
            raise ValueError("deadline must be a date")

    def days_left(self, today: date) -> int:
        """Return remaining days until deadline, never below zero.

        Args:
            today: Reference date for calculating remaining days.

        Returns:
            Number of days left (non-negative integer).
        """
        return max((self.deadline - today).days, 0)
