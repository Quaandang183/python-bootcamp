"""Input/output utilities for reading tasks from CSV and persisting to JSON."""

import csv
import json
from datetime import date
from pathlib import Path

try:
    from .models import Task
except ImportError:
    from models import Task


def load_tasks(path: str | Path) -> list[Task]:
    """Load tasks from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        A list of Task objects.

    Raises:
        ValueError: If data on any line is malformed or missing required columns.
    """
    tasks: list[Task] = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # Header is line 1, data starts at line 2
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
            except (KeyError, ValueError, TypeError) as e:
                # Keep 'line {idx}' so test assertions match line number reporting
                raise ValueError(f"Dữ liệu không hợp lệ tại line {idx}: {e}") from e
    return tasks


def save_json(tasks: list[Task], path: str | Path) -> None:
    """Save tasks list to a JSON file.

    Args:
        tasks: List of Task objects.
        path: Output destination path.
    """
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