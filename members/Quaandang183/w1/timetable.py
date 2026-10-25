"""W1-5: group a timetable by day."""


def by_day(entries: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group ``(course, day)`` pairs by day, with the courses of each day sorted."""
    result: dict[str, list[str]] = {}
    for course, day in entries:
        result.setdefault(day, []).append(course)
    return {day: sorted(courses) for day, courses in result.items()}
