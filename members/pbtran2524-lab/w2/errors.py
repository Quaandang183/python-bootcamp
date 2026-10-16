class InfeasiblePlan(Exception):
    """Ngoại lệ riêng khi kế hoạch vượt quá quỹ thời gian cho phép."""
    pass


def check_feasible(tasks: list, available_h: float) -> None:
    """Kiểm tra quỹ thời gian có đủ thực hiện các nhiệm vụ hay không.
    
    Phát sinh lỗi InfeasiblePlan nếu tổng thời gian vượt quá available_h.
    """
    total_hours = sum(task.duration for task in tasks)
    if total_hours > available_h:
        raise InfeasiblePlan(
            f"Kế hoạch không khả thi: Tổng thời gian cần ({total_hours}h) "
            f"vượt quá quỹ thời gian có sẵn ({available_h}h)."
        )