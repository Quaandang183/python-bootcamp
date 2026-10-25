"""Schedule organization utilities for grouping courses by day."""


def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day of the week and sort courses alphabetically.

    Args:
        timetable: List of tuples (course_code, day_of_week).

    Returns:
        A dictionary mapping each day to a sorted list of course codes.
    """
    result = {}

    for course, day in timetable:
        result.setdefault(day, []).append(course)

    for courses in result.values():
        courses.sort()

    return result

