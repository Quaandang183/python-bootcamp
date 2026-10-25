"""Module defining academic rules and requirements for thesis registration."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check if a student meets the eligibility criteria for thesis registration.

    Criteria require at least 120 completed credits and a minimum GPA of 2.0.

    Args:
        credits (int): The total number of completed academic credits.
        gpa (float): The current Grade Point Average (GPA).

    Returns:
        bool: True if eligible for thesis registration, False otherwise.
    """
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Generate a list of specific reasons explaining missing thesis eligibility requirements.

    Args:
        credits (int): The total number of completed academic credits.
        gpa (float): The current Grade Point Average (GPA).

    Returns:
        list[str]: A list of text descriptions specifying unfulfilled requirements.
    """
    reasons = []

    if credits < 120:
        needed_credits = 120 - credits
        reasons.append(f"need {needed_credits} more credits")

    if gpa < 2.0:
        reasons.append("need higher GPA (at least 2.0)")

    return reasons