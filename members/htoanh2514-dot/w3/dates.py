"""Module for parsing relative and absolute due dates."""

from datetime import date, timedelta
import re

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_due(due_str: str, today: date) -> date:
    """Parse a date string (ISO format, relative, or weekday) relative to today.

    Args:
        due_str: The due date representation (e.g., '2026-10-30', 'tomorrow', 'in 3 days', 'Fri').
        today: The base reference date.

    Returns:
        The calculated target date.

    Raises:
        ValueError: If the date format cannot be parsed.
    """
    clean_str = due_str.strip()

    # 1. Định dạng ISO: YYYY-MM-DD
    try:
        return date.fromisoformat(clean_str)
    except ValueError:
        pass

    # 2. 'tomorrow'
    if clean_str.lower() == "tomorrow":
        return today + timedelta(days=1)

    # 3. 'in X days'
    match_in_days = re.fullmatch(r"in\s+(\d+)\s+days?", clean_str, re.IGNORECASE)
    if match_in_days:
        days = int(match_in_days.group(1))
        return today + timedelta(days=days)

    # 4. Thứ trong tuần (VD: Fri, Tue) - Lấy ngày tiếp theo trong tương lai
    for idx, day_name in enumerate(WEEKDAYS):
        if clean_str.lower().startswith(day_name.lower()):
            days_ahead = idx - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)

    raise ValueError(f"Invalid due date format: '{due_str}'")