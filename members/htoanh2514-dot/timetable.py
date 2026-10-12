from collections import defaultdict


def group_timetable(timetable: list) -> dict:
  """Gom nhóm danh sách các môn học theo từng ngày, các môn học trong mỗi ngày được sắp xếp."""
  timetable_dict = defaultdict(list)

  for course, day in timetable:
    timetable_dict[day].append(course)

  for day in timetable_dict:
    timetable_dict[day].sort()

  return dict(timetable_dict)