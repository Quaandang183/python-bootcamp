"""Command-line tool for generating a study plan within available hours."""

import argparse
import sys
from datetime import date
from pathlib import Path

try:
    from ..w2.io_utils import load_tasks
    from ..w2.models import Task
except (ImportError, ValueError):
    from members.NgoGiaBao279.w2.io_utils import load_tasks
    from members.NgoGiaBao279.w2.models import Task


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a daily study plan based on task priorities and available hours."
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to the tasks CSV file.",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Total available study hours for tonight.",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Reference date in YYYY-MM-DD format (default: today).",
    )
    return parser.parse_args(args)


def prioritise_tasks(tasks: list[Task], today: date) -> list[Task]:
    """Sort tasks by decreasing urgency/importance ratio, preserving order on ties."""
    return sorted(
        tasks,
        key=lambda task: task.importance / max(task.days_left(today), 1),
        reverse=True,
    )


def allocate_time(
    tasks: list[Task], available_hours: float
) -> list[tuple[Task, float]]:
    """Allocate available study hours across prioritized tasks."""
    remaining = available_hours
    schedule: list[tuple[Task, float]] = []

    for task in tasks:
        if remaining <= 0:
            break
        effort = getattr(task, "effort_h", getattr(task, "duration", 0.0))
        time_block = min(effort, remaining)
        if time_block > 0:
            schedule.append((task, time_block))
            remaining -= time_block

    return schedule


def render_schedule(schedule: list[tuple[Task, float]], hours: float) -> str:
    """Format the allocated study schedule as a readable string."""
    lines = [f"Tonight ({hours:.1f} h):"]
    for idx, (task, allocated_h) in enumerate(schedule, start=1):
        prefix = f"  {idx}. {task.title} "
        dots = "." * max(2, 22 - len(prefix))
        lines.append(f"{prefix}{dots} {allocated_h:.1f} h")
    return "\n".join(lines)


def main(args: list[str] | None = None) -> int:
    """Run the CLI application."""
    parsed = parse_args(args)

    if not parsed.csv_path.is_file():
        print(f"Error: File '{parsed.csv_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        tasks = load_tasks(parsed.csv_path)
    except (OSError, ValueError) as err:
        print(f"Error loading tasks from '{parsed.csv_path}': {err}", file=sys.stderr)
        return 1

    prioritised = prioritise_tasks(tasks, today=parsed.today)
    schedule = allocate_time(prioritised, available_hours=parsed.hours)
    output = render_schedule(schedule, hours=parsed.hours)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
