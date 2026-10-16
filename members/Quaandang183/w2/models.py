from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        if not 1 <= self.importance <= 5:
            raise ValueError(f"importance must be 1-5, got {self.importance}")
        if self.effort_h <= 0:
            raise ValueError(f"effort_h must be positive, got {self.effort_h}")

    def days_left(self, today: date) -> int:
        return max((self.deadline - today).days, 0)
