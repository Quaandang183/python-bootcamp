from dataclasses import dataclass
from datetime import date
from math import isfinite


@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self):
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
        """Return remaining days, never below zero."""
        return max((self.deadline - today).days, 0)