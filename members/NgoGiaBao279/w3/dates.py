"""Date parsing utilities for deadlines."""

import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Parse relative or absolute date strings into a date object.

    Accepts:
      - ISO dates: "YYYY-MM-DD" (e.g. "2026-10-30")
      - "today", "tomorrow"
      - "in N days" (e.g. "in 3 days")
      - Weekday names (e.g. "Fri", "Tue", "monday") which resolve to the
        next occurrence strictly after `today`.

    Raises:
      ValueError: If the date format is unsupported or invalid.
    """
    clean_text = text.strip()
    lower_text = clean_text.lower()

    if lower_text == "today":
        return today

    if lower_text == "tomorrow":
        return today + timedelta(days=1)

    in_days_match = re.fullmatch(r"in\s+(\d+)\s+days?", lower_text)
    if in_days_match:
        days = int(in_days_match.group(1))
        return today + timedelta(days=days)

    weekdays_short = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    weekdays_full = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    target_weekday = None
    if lower_text in weekdays_short:
        target_weekday = weekdays_short.index(lower_text)
    elif lower_text in weekdays_full:
        target_weekday = weekdays_full.index(lower_text)

    if target_weekday is not None:
        offset = (target_weekday - today.weekday()) % 7
        if offset == 0:
            offset = 7
        return today + timedelta(days=offset)

    try:
        return date.fromisoformat(clean_text)
    except ValueError as e:
        raise ValueError(f"Unknown date format: {text!r}") from e
