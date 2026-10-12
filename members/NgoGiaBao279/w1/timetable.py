from collections import defaultdict


def group_timetable(timetable):

    grouped = defaultdict(list)
    
    for course, day in timetable:
        grouped[day].append(course)
        
    for day in grouped:
        grouped[day].sort()
        
    return dict(grouped)


if __name__ == "__main__":
    sample_timetable = [
        ("Math", "Monday"),
        ("Physics", "Tuesday"),
        ("English", "Monday"),
        ("Chemistry", "Wednesday"),
        ("Programming", "Tuesday")
    ]
    
    result = group_timetable(sample_timetable)
    print (result)
