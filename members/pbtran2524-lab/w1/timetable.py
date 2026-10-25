"""Timetable grouping module.

This module provides utilities to organize timetable entries by day, returning
a dictionary where each day maps to a sorted list of course names.
"""

from collections import defaultdict


def group_timetable(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day and sort course names alphabetically within each day.

    Args:
        timetable (list[tuple[str, str]]): A list of tuples, where each tuple
            contains `(course_name, day_of_week)`.

    Returns:
        dict[str, list[str]]: A dictionary mapping each day string to an
            alphabetically sorted list of course names scheduled for that day.
    """
    grouped = defaultdict(list)

    for course, day in timetable:
        grouped[day].append(course)

    for day in grouped:
        grouped[day].sort()

    return dict(grouped)