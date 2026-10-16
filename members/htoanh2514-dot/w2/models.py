from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    title: str
    duration: float
    importance: int
    deadline: date

    def __post_init__(self):
        # Kiểm tra giá trị importance phải nằm trong khoảng từ 1 đến 5
        if not (1 <= self.importance <= 5):
            raise ValueError(f"Importance phải nằm trong khoảng 1-5, nhận được: {self.importance}")

    def days_left(self, today: date) -> int:
        delta = (self.deadline - today).days
        return max(0, delta)