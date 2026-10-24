"""Shared dataclasses and contracts for study planner."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Task item contract."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    @property
    def name(self) -> str:
        """Alias for title to maintain backward compatibility."""
        return self.title

    @property
    def duration(self) -> float:
        """Alias for effort_h to maintain backward compatibility."""
        return self.effort_h


@dataclass
class Block:
    """Scheduled time block contract."""

    task: Task
    hours: float