"""Module for file I/O operations including CSV parsing and JSON exports."""

import csv
import json
from datetime import datetime, date
from typing import Any
from .models import Task


def load_tasks(path: Any) -> list[Task]:
    """Parse a CSV file and load a list of Task objects.

    Args:
        path (str | Path): The file path to the CSV file containing task records.

    Returns:
        list[Task]: A list of instantiated Task objects.

    Raises:
        ValueError: If a row contains invalid data types or missing fields, 
                    including the specific line number in the exception message.
    """
    tasks = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # Header is line 1, data starts at line 2
            try:
                title = row["title"]
                importance = int(row["importance"])
                duration = float(row["duration"])
                deadline = datetime.strptime(row["deadline"].strip(), "%Y-%m-%d").date()
                tasks.append(Task(title=title, importance=importance, duration=duration, deadline=deadline))
            except Exception as e:
                # Required error message containing 'line <line_number>' for test assertions
                raise ValueError(f"Dữ liệu không hợp lệ tại line {idx}: {e}")
    return tasks


def save_json(tasks: list[Task], path: Any) -> None:
    """Serialize a list of Task objects and write them to a JSON file.

    Args:
        tasks (list[Task]): The list of Task objects to export.
        path (str | Path): The target file path for saving the JSON output.
    """
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