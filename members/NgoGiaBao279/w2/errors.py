"""Custom exceptions and validation for study planner."""


class InfeasiblePlan(Exception):
    """Ngoại lệ phát sinh khi tổng thời gian thực hiện kế hoạch vượt quá thời gian cho phép."""
    def __init__(self, needed_h: float, available_h: float, message: str = None):
        self.needed_h = needed_h
        self.available_h = available_h
        if message is None:
            message = (
                f"Kế hoạch không khả thi: Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng."
            )
        super().__init__(message)


def check_feasible(tasks: list, available_h: float) -> None:
    """Kiểm tra tính khả thi của danh sách công việc so với số giờ khả dụng."""
    needed_h = sum(
        getattr(t, "duration", getattr(t, "effort_h", getattr(t, "hours", 0.0)))
        for t in tasks
    )
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)