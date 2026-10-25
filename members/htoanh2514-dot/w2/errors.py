class InfeasiblePlan(Exception):
    """Exception raised when a study plan is infeasible due to insufficient available time.

    Attributes:
        needed_h (float): Total study hours required to complete all tasks.
        available_h (float): Total study hours available.
    """

    def __init__(self, needed_h: float, available_h: float, message: str = None) -> None:
        """Initialize InfeasiblePlan with time metrics and custom error message.

        Args:
            needed_h (float): Total required hours.
            available_h (float): Available hours.
            message (str, optional): Custom error message. Defaults to None.
        """
        self.needed_h = needed_h
        self.available_h = available_h
        if message is None:
            message = f"Cần {needed_h}h nhưng chỉ có {available_h}h khả dụng."
        super().__init__(message)


def check_feasible(tasks: list, available_h: float) -> None:
    """Validate whether the total task duration fits within the available hours.

    Args:
        tasks (list): List of task objects, where each task has a 'duration' attribute.
        available_h (float): Total study hours available.

    Raises:
        InfeasiblePlan: If the total duration required exceeds available hours.
    """
    needed_h = sum(t.duration for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)