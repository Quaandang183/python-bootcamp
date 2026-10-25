"""Task data model representation."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Đại diện cho một nhiệm vụ cần thực hiện."""

    title: str = "Untitled"
    importance: int = 1
    duration: float = 0.0
    deadline: date = None

    def __post_init__(self):
        """Kiểm tra tính hợp lệ của các trường sau khi khởi tạo."""
        if not (1 <= self.importance <= 5):
            raise ValueError(f"Importance phải nằm trong khoảng 1-5, nhận được: {self.importance}")
        if self.duration < 0:
            raise ValueError(f"Duration không được là số âm, nhận được: {self.duration}")

    @property
    def name(self) -> str:
        """Thuộc tính tên nhiệm vụ (alias của title)."""
        return self.title

    @property
    def effort_h(self) -> float:
        """Thuộc tính thời lượng nhiệm vụ (alias của duration)."""
        return self.duration

    def days_left(self, today: date) -> int:
        """Tính số ngày còn lại đến hạn chót so với ngày tham chiếu."""
        if self.deadline is None:
            return 0
        delta = (self.deadline - today).days
        return max(0, delta)