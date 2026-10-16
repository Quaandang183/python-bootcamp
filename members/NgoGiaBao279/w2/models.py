from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str = "Untitled"
    importance: int = 1
    duration: float = 0.0
    deadline: date = None

    def __post_init__(self):
        if not (1 <= self.importance <= 5):
            raise ValueError(f"Importance phải nằm trong khoảng 1-5, nhận được: {self.importance}")
        if self.duration < 0:
            raise ValueError(f"Duration không được là số âm, nhận được: {self.duration}")

    @property
    def name(self) -> str:
        return self.title

    @property
    def effort_h(self) -> float:
        return self.duration

    def days_left(self, today: date) -> int:
        if self.deadline is None:
            return 0
        delta = (self.deadline - today).days
        return max(0, delta)