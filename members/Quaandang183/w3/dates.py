"""W3-1: parse human-friendly due dates."""

import re
from datetime import date, timedelta

WEEKDAYS = {
    "mon": 0, "monday": 0,
    "tue": 1, "tues": 1, "tuesday": 1,
    "wed": 2, "wednesday": 2,
    "thu": 3, "thur": 3, "thurs": 3, "thursday": 3,
    "fri": 4, "friday": 4,
    "sat": 5, "saturday": 5,
    "sun": 6, "sunday": 6,
}  # fmt: skip

ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
IN_DAYS = re.compile(r"in (\d+) days?")


def parse_due(text: str, today: date) -> date:
    """Turn ``text`` into a date, relative to ``today``.

    Accepted forms: ``2026-10-30``, ``today``, ``tomorrow``, ``in 3 days`` and weekday
    names such as ``Fri`` or ``friday`` (the next occurrence, never today).
    Anything else raises ValueError.
    """
    t = " ".join(text.lower().split())

    if ISO_DATE.fullmatch(t):
        return date.fromisoformat(t)  # ValueError for impossible dates such as 2026-13-45
    if t == "today":
        return today
    if t == "tomorrow":
        return today + timedelta(days=1)

    match = IN_DAYS.fullmatch(t)
    if match:
        return today + timedelta(days=int(match.group(1)))

    if t in WEEKDAYS:
        ahead = (WEEKDAYS[t] - today.weekday()) % 7 or 7  # same weekday -> next week
        return today + timedelta(days=ahead)

    raise ValueError(f"cannot understand due date: {text!r}")
