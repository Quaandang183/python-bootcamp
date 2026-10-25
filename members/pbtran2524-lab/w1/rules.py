"""Thesis registration eligibility module.

This module provides utility functions to check student qualification status
for graduation thesis registration and determine missing requirements.
"""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Determine whether a student satisfies the criteria to register for a thesis.

    Args:
        credits (int): Total number of completed academic credits.
        gpa (float): Current Grade Point Average on a 4.0 scale.

    Returns:
        bool: True if credits are at least 120 and GPA is at least 2.0; False otherwise.
    """
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Identify specific unmet requirements for thesis registration eligibility.

    Args:
        credits (int): Total number of completed academic credits.
        gpa (float): Current Grade Point Average on a 4.0 scale.

    Returns:
        list[str]: A list of human-readable error messages explaining missing
            prerequisites (e.g., remaining credits needed, GPA shortfall).
            Returns an empty list if all prerequisites are satisfied.
    """
    reasons = []

    if credits < 120:
        needed_credits = 120 - credits
        reasons.append(f"need {needed_credits} more credits")

    if gpa < 2.0:
        reasons.append("gpa must be at least 2.0")

    return reasons