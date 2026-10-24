class InfeasiblePlan(Exception):
    pass

def check_feasible(tasks: list, available_h: float) -> None:
    total_hours = sum(task.duration for task in tasks)
    if total_hours > available_h:
        raise InfeasiblePlan(
            f"Kế hoạch không khả thi: Tổng thời gian cần ({total_hours}h) "
            f"vượt quá quỹ thời gian có sẵn ({available_h}h)."
        )