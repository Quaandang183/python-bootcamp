"""W2-3: ngoại lệ tùy chỉnh cho kế hoạch không khả thi."""


class InfeasiblePlan(Exception):
    """Tổng số giờ cần thiết vượt quá số giờ có sẵn."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        super().__init__(needed_h, available_h)
        self.needed_h = needed_h
        self.available_h = available_h

    def __str__(self) -> str:
        return (
            f"Plan is infeasible: needs {self.needed_h:g}h "
            f"but only {self.available_h:g}h available"
        )


def check_feasible(tasks, available_h: float) -> None:
    """Raise InfeasiblePlan nếu tổng effort_h của tasks > available_h."""
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
