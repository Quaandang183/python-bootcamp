try:
    from .errors import InfeasiblePlan, check_feasible
except ImportError:
    from errors import InfeasiblePlan, check_feasible

__all__ = ["InfeasiblePlan", "check_feasible"]
