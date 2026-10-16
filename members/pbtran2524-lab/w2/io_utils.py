from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    name: str
    duration: float
    importance: int
    deadline: date

    def days_left(self, today: date) -> int:
        """Tính số ngày còn lại từ today đến deadline.

        Giá trị trả về không bao giờ nhỏ hơn 0.
        """
        remaining_days = (self.deadline - today).days
        return max(0, remaining_days)