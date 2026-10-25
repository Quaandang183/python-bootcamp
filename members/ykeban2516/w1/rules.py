"""Academic graduation and thesis registration eligibility rules."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check whether a student satisfies thesis registration requirements.

    Args:
        credits: Total accumulated credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        True if credits >= 120 and gpa >= 2.0, False otherwise.
    """
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Identify unmet criteria preventing thesis registration.

    Args:
        credits: Total accumulated credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        A list of explanation strings for each missing condition.
    """
    reasons = []

    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")

    if gpa < 2.0:
        reasons.append("need GPA of at least 2.0")

    return reasons

