"""W2-2: đọc CSV và ghi JSON."""
import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .models import Task

FIELDS = ("title", "importance", "effort_h", "deadline")


def load_tasks(path: str | Path) -> list[Task]:
    """Đọc file CSV (header: title,importance,effort_h,deadline).

    Dòng không hợp lệ sẽ raise ValueError kèm số dòng trong file.
    """
    tasks: list[Task] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or set(FIELDS) - set(reader.fieldnames):
            raise ValueError(f"line 1: header must contain {','.join(FIELDS)}")
        for line_no, row in enumerate(reader, start=2):
            try:
                tasks.append(
                    Task(
                        title=row["title"].strip(),
                        importance=int(row["importance"]),
                        effort_h=float(row["effort_h"]),
                        deadline=date.fromisoformat(row["deadline"].strip()),
                    )
                )
            except (ValueError, TypeError, AttributeError) as e:
                raise ValueError(f"line {line_no}: invalid row ({e})") from e
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Ghi danh sách Task ra file JSON (deadline dạng YYYY-MM-DD)."""
    data = []
    for t in tasks:
        d = asdict(t)
        d["deadline"] = t.deadline.isoformat()
        data.append(d)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
