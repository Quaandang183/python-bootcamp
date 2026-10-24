import csv
import json
from datetime import date
try:
    from .models import Task
except ImportError:
    from models import Task


def load_tasks(path) -> list[Task]:
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # Dòng 1 là tiêu đề (header), dữ liệu bắt đầu từ dòng 2
            try:
                clean_row = {str(k).strip().lower(): str(v).strip() for k, v in row.items() if k is not None}
                title = clean_row.get("title") or clean_row.get("name") or "Untitled"
                importance = int(clean_row.get("importance", 1))
                duration = float(clean_row.get("duration") or clean_row.get("effort_h") or 0.0)
                
                if "deadline" not in clean_row:
                    raise KeyError("Thiếu cột deadline")
                deadline = date.fromisoformat(clean_row["deadline"])
                
                task = Task(title=title, importance=importance, duration=duration, deadline=deadline)
                tasks.append(task)
            except Exception as e:
                # Đảm bảo chứa 'line {idx}' để vừa đáp ứng yêu cầu số thứ tự dòng vừa khớp kiểm thử
                raise ValueError(f"Dữ liệu không hợp lệ tại line {idx}: {e}")
    return tasks


def save_json(tasks: list[Task], path) -> None:
    data = []
    for t in tasks:
        item = {
            "title": t.title,
            "importance": t.importance,
            "duration": t.duration,
            "deadline": t.deadline.isoformat() if isinstance(t.deadline, date) else str(t.deadline),
        }
        data.append(item)

    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)