import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .models import Task


def load_tasks(path) -> list[Task]:
    tasks = []

    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, strict=True)

        try:
            header = next(reader)
        except StopIteration as error:
            raise ValueError("line 1: missing CSV header") from error
        except csv.Error as error:
            raise ValueError(f"line 1: {error}") from error

        if header != ["title", "importance", "effort_h", "deadline"]:
            raise ValueError("line 1: invalid CSV header")

        while True:
            line_number = reader.line_num + 1

            try:
                row = next(reader)
            except StopIteration:
                break
            except csv.Error as error:
                raise ValueError(
                    f"line {line_number}: {error}"
                ) from error

            if not row:
                continue

            try:
                if len(row) != 4:
                    raise ValueError("expected four columns")

                title, importance, effort_h, deadline = row

                task = Task(
                    title=title.strip(),
                    importance=int(importance),
                    effort_h=float(effort_h),
                    deadline=date.fromisoformat(deadline.strip()),
                )
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"line {line_number}: {error}"
                ) from error

            tasks.append(task)

    return tasks


def save_json(tasks: list[Task], path) -> None:
    records = []

    for task in tasks:
        record = asdict(task)
        record["deadline"] = task.deadline.isoformat()
        records.append(record)

    with Path(path).open("w", encoding="utf-8") as destination:
        json.dump(
            records,
            destination,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        destination.write("\n")