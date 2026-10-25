"""Course timetable organization and grouping utilities."""

from collections import defaultdict


def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day of the week, with course codes sorted alphabetically.

    Args:
        timetable: A list of (course_code, day_name) tuples.

    Returns:
        A dictionary mapping each day to its sorted list of course codes.
    """
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for course, day in timetable:
        grouped[day].append(course)

    for day in grouped:
        grouped[day].sort()

    return dict(grouped)


group_timetable = by_day

if __name__ == "__main__":
    sample_timetable = [
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon"),
    ]
    print(by_day(sample_timetable))
