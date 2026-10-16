from collections import defaultdict


def group_timetable(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    grouped = defaultdict(list)

    for course, day in timetable:
        grouped[day].append(course)

    for day in grouped:
        grouped[day].sort()

    return dict(grouped)