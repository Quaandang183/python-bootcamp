"""Custom exceptions and plan feasibility validation."""


class InfeasiblePlan(Exception):
    """Exception raised when planned study hours exceed available time.

    Attributes:
        needed_h: Total needed effort in hours.
        available_h: Total available hours.
    """

    def __init__(self, needed_h: float, available_h: float, message: str | None = None) -> None:
        """Initialize InfeasiblePlan with needed and available hours.

        Args:
            needed_h: Total required hours.
            available_h: Available capacity in hours.
            message: Optional custom error message.
        """
        self.needed_h = needed_h
        self.available_h = available_h
        if message is None:
            message = (
                f"Kế hoạch không khả thi: Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng."
            )
        super().__init__(message)


def check_feasible(tasks: list, available_h: float) -> None:
    """Validate whether the task list fits within the available hours.

    Args:
        tasks: A list of task objects containing duration or effort_h.
        available_h: Total available capacity in hours.

    Raises:
        InfeasiblePlan: If needed hours strictly exceed available hours.
    """
    needed_h = sum(
        getattr(t, "duration", getattr(t, "effort_h", getattr(t, "hours", 0.0)))
        for t in tasks
    )
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)