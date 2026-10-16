def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    reasons = []

    if credits < 120:
        needed_credits = 120 - credits
        reasons.append(f"need {needed_credits} more credits")

    if gpa < 2.0:
        reasons.append("gpa must be at least 2.0")

    return reasons