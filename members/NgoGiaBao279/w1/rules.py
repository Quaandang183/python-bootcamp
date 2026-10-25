"""Thesis registration rules and prerequisite checks."""

MIN_CREDITS = 120
MIN_GPA = 2.0


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Check if student meets minimum credit and GPA criteria to register a thesis.

    Args:
        credits: Total completed academic credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        True if eligible, False otherwise.
    """
    return credits >= MIN_CREDITS and gpa >= MIN_GPA


def missing(credits: int, gpa: float) -> list[str]:
    """List unmet criteria for registering a thesis.

    Args:
        credits: Total completed academic credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        A list of missing condition strings, or an empty list if fully eligible.
    """
    reasons: list[str] = []
    if credits < MIN_CREDITS:
        reasons.append(f"need {MIN_CREDITS - credits} more credits")
    if gpa < MIN_GPA:
        reasons.append(f"need GPA of at least {MIN_GPA} (currently {gpa})")
    return reasons


if __name__ == "__main__":
    test_credits = 115
    test_gpa = 1.9
    print("Có đủ điều kiện đăng ký khóa luận không?:", can_register_thesis(test_credits, test_gpa))
    print("Các lý do chưa đạt:", missing(test_credits, test_gpa))