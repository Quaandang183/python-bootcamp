"""W1-3: thesis registration rules."""

MIN_CREDITS = 120
MIN_GPA = 2.0


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return True if the student has enough credits and a high enough GPA."""
    return credits >= MIN_CREDITS and gpa >= MIN_GPA


def missing(credits: int, gpa: float) -> list[str]:
    """List every reason why the student cannot register yet (empty if none)."""
    reasons: list[str] = []
    if credits < MIN_CREDITS:
        reasons.append(f"need {MIN_CREDITS - credits} more credits")
    if gpa < MIN_GPA:
        reasons.append(f"need GPA of at least {MIN_GPA} (currently {gpa})")
    return reasons
