import csv
import json
from datetime import datetime, date
from .models import Task

def load_tasks(path) -> list[Task]:
    tasks = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # Dòng 1 là header, dữ liệu bắt đầu từ dòng 2
            try:
                title = row["title"]
                importance = int(row["importance"])
                duration = float(row["duration"])
                deadline = datetime.strptime(row["deadline"].strip(), "%Y-%m-%d").date()
                tasks.append(Task(title=title, importance=importance, duration=duration, deadline=deadline))
            except Exception as e:
                # Bắt buộc thông báo lỗi chứa từ "line <số_dòng>" để khớp với test (match="line 3")
                raise ValueError(f"Dữ liệu không hợp lệ tại line {idx}: {e}")
    return tasks

def save_json(tasks: list[Task], path) -> None:
    data = []
    for t in tasks:
        data.append({
            "title": t.title,
            "importance": t.importance,
            "duration": t.duration,
            "deadline": t.deadline.strftime("%Y-%m-%d") if isinstance(t.deadline, date) else str(t.deadline)
        })
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)