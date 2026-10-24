"""Parse explicit dates and simple relative deadlines."""

import re
from datetime import date, timedelta


def parse_due(text: str, today: date) -> date:
    """Resolve a deadline; weekday names always mean the next occurrence."""
    value = text.strip().lower()
    if value == "today":
        return today
    if value == "tomorrow":
        return today + timedelta(days=1)

    match = re.fullmatch(r"in (\d+) days?", value)
    if match:
        return today + timedelta(days=int(match.group(1)))

    weekdays = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
    if value in weekdays:
        offset = (weekdays.index(value) - today.weekday()) % 7 or 7
        return today + timedelta(days=offset)

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return date.fromisoformat(value)

    raise ValueError(f"Unsupported deadline: {text!r}")
