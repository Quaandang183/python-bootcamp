"""W2-1: the Task model."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """A study task with an importance (1-5), an effort in hours and a deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Reject an importance outside 1-5 or a non-positive effort."""
        if not 1 <= self.importance <= 5:
            raise ValueError(f"importance must be 1-5, got {self.importance}")
        if self.effort_h <= 0:
            raise ValueError(f"effort_h must be positive, got {self.effort_h}")

    def days_left(self, today: date) -> int:
        """Days from ``today`` to the deadline, never below 0."""
        return max((self.deadline - today).days, 0)
