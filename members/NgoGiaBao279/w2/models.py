"""Task data model representation."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represents a scheduled learning task.

    Attributes:
        title: Title/name of the task.
        importance: Priority score from 1 (low) to 5 (high).
        duration: Required completion time in hours.
        deadline: Deadline date object.
    """

    title: str = "Untitled"
    importance: int = 1
    duration: float = 0.0
    deadline: date | None = None

    def __post_init__(self) -> None:
        """Validate task fields after dataclass initialization."""
        if not (1 <= self.importance <= 5):
            raise ValueError(f"Importance phải nằm trong khoảng 1-5, nhận được: {self.importance}")
        if self.duration < 0:
            raise ValueError(f"Duration không được là số âm, nhận được: {self.duration}")

    @property
    def name(self) -> str:
        """Alias for title to maintain backward compatibility."""
        return self.title

    @property
    def effort_h(self) -> float:
        """Alias for duration to match shared contract."""
        return self.duration

    def days_left(self, today: date) -> int:
        """Calculate the remaining days from today until deadline.

        Args:
            today: Reference date object.

        Returns:
            Remaining days (non-negative integer).
        """
        if self.deadline is None:
            return 0
        delta = (self.deadline - today).days
        return max(0, delta)