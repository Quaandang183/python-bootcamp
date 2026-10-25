"""Date parsing utilities for deadlines."""

import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Parse a date string or relative deadline into a concrete date object.

    Accepts:
    - ISO format: "YYYY-MM-DD" (e.g., "2026-10-30")
    - Relative shortcuts: "today", "tomorrow"
    - Relative offset: "in X day" / "in X days" (e.g., "in 3 days")
    - Weekday abbreviations or names: "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
      (always resolves to the next occurrence strictly after today)

    Raises:
        ValueError: If text cannot be parsed or format is unknown.
    """
    clean_text = text.strip().lower()

    if clean_text == "today":
        return today
    if clean_text == "tomorrow":
        return today + timedelta(days=1)

    in_days_match = re.fullmatch(r"in\s+(\d+)\s+days?", clean_text)
    if in_days_match:
        days = int(in_days_match.group(1))
        return today + timedelta(days=days)

    weekdays = {
        "mon": 0,
        "monday": 0,
        "tue": 1,
        "tuesday": 1,
        "wed": 2,
        "wednesday": 2,
        "thu": 3,
        "thursday": 3,
        "fri": 4,
        "friday": 4,
        "sat": 5,
        "saturday": 5,
        "sun": 6,
        "sunday": 6,
    }
    if clean_text in weekdays:
        target_wd = weekdays[clean_text]
        offset = (target_wd - today.weekday()) % 7
        if offset == 0:
            offset = 7
        return today + timedelta(days=offset)

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", clean_text):
        try:
            return date.fromisoformat(clean_text)
        except ValueError as err:
            raise ValueError(f"Invalid date value: {text}") from err

    raise ValueError(f"Unknown or unsupported date expression: {text!r}")
