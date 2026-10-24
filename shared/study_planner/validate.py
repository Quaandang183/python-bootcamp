try:
    from shared.contract import Task
except ImportError:
    from contract import Task


class InfeasiblePlan(Exception):
    """Ngoại lệ phát sinh khi kế hoạch không khả thi (tổng thời gian cần vượt quá thời gian khả dụng)."""

    def __init__(self, needed_h: float, available_h: float, message: str | None = None):
        self.needed_h = needed_h
        self.available_h = available_h
        if message is None:
            message = (
                f"Kế hoạch không khả thi: Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng."
            )
        super().__init__(message)


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Kiểm tra tổng thời gian thực hiện các nhiệm vụ so với quỹ thời gian khả dụng.
    
    Phát sinh InfeasiblePlan nếu needed_h > available_h.
    """
    needed_h = sum(
        getattr(t, "effort_h", getattr(t, "duration", getattr(t, "hours", 0.0)))
        for t in tasks
    )
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)
