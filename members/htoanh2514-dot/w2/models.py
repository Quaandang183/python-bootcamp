"""Module defining core data models for the study planner application."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represent a study task with priority constraints and deadline tracking.

    Attributes:
        title (str): The descriptive title of the task.
        duration (float): Estimated effort required in hours.
        importance (int): Task priority level ranging strictly from 1 to 5.
        deadline (date): Due date for task completion.
    """

    title: str
    duration: float
    importance: int
    deadline: date

    def __post_init__(self) -> None:
        """Validate attribute bounds after dataclass initialization.

        Raises:
            ValueError: If importance is not between 1 and 5 (inclusive).
        """
        # Validate that importance score falls within the allowed 1-5 scale
        if not (1 <= self.importance <= 5):
            raise ValueError(f"Importance phải nằm trong khoảng 1-5, nhận được: {self.importance}")

    def days_left(self, today: date) -> int:
        """Calculate remaining days until task deadline relative to a given date.

        Args:
            today (date): The baseline reference date.

        Returns:
            int: Number of days remaining, returning 0 if the deadline has passed.
        """
        delta = (self.deadline - today).days
        return max(0, delta)