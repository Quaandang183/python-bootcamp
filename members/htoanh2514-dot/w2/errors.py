class InfeasiblePlan(Exception):
    """Ngoại lệ phát sinh khi kế hoạch không khả thi."""
    def __init__(self, needed_h: float, available_h: float, message: str = None):
        self.needed_h = needed_h
        self.available_h = available_h
        if message is None:
            message = f"Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng."
        super().__init__(message)

def check_feasible(tasks: list, available_h: float) -> None:
    needed_h = sum(t.duration for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)