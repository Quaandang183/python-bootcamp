"""Module for timetable processing and schedule organization."""

from collections import defaultdict


def group_timetable(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day and sort course names alphabetically within each day.

    Args:
        timetable (list[tuple[str, str]]): A list of tuples, where each tuple 
            contains (course_name, day_of_week).

    Returns:
        dict[str, list[str]]: A dictionary mapping days of the week to 
            alphabetically sorted lists of course names.
    """
    timetable_dict = defaultdict(list)

    # Group course names under their respective days
    for course, day in timetable:
        timetable_dict[day].append(course)

    # Sort courses alphabetically for each day
    for day in timetable_dict:
        timetable_dict[day].sort()

    return dict(timetable_dict)