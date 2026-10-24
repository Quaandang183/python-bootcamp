"""Command-line tool to schedule study tasks within a time budget."""

import argparse
import sys
from datetime import date
from pathlib import Path

try:
    from members.NgoGiaBao279.w2.io_utils import load_tasks
    from members.NgoGiaBao279.w2.models import Task
except ImportError:
    try:
        from ..w2.io_utils import load_tasks
        from ..w2.models import Task
    except ImportError:
        from io_utils import load_tasks  # type: ignore
        from models import Task  # type: ignore


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional list of argument strings.

    Returns:
        argparse.Namespace: Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        description="Allocate study tasks within available study hours."
    )
    parser.add_argument(
        "csv_path",
        type=str,
        help="Path to the tasks CSV file",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study hours",
    )
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Current date as reference (YYYY-MM-DD, default: today)",
    )
    return parser.parse_args(argv)


def allocate_tasks(
    tasks: list[Task], hours: float, today: date
) -> list[tuple[Task, float]]:
    """Prioritise and allocate time blocks to tasks.

    Args:
        tasks: List of Task objects.
        hours: Total hours available.
        today: Reference date for urgency calculation.

    Returns:
        list[tuple[Task, float]]: Allocated tasks with their assigned hours.
    """
    ordered = sorted(
        tasks,
        key=lambda task: task.importance / max(task.days_left(today), 1),
        reverse=True,
    )

    remaining = hours
    allocated: list[tuple[Task, float]] = []

    for task in ordered:
        if remaining <= 0:
            break
        duration = getattr(task, "duration", getattr(task, "effort_h", 0.0))
        time_to_give = min(duration, remaining)
        if time_to_give > 0:
            allocated.append((task, time_to_give))
            remaining -= time_to_give

    return allocated


def format_plan(allocated: list[tuple[Task, float]], hours: float) -> str:
    """Format allocated tasks into a pretty table.

    Args:
        allocated: List of (Task, allocated_hours) pairs.
        hours: Total available hours.

    Returns:
        str: Formatted plan output.
    """
    lines = [f"Tonight ({hours:.1f} h):"]
    target_width = 28

    for idx, (task, allocated_h) in enumerate(allocated, start=1):
        prefix = f"  {idx}. {task.title} "
        suffix = f" {allocated_h:.1f} h"
        dots_count = max(2, target_width - len(prefix) - len(suffix))
        lines.append(f"{prefix}{'.' * dots_count}{suffix}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Run the CLI application.

    Args:
        argv: Optional command-line argument list.

    Returns:
        int: Exit status code (0 for success, 1 for errors).
    """
    args = parse_args(argv)
    csv_file = Path(args.csv_path)

    if not csv_file.is_file():
        sys.stderr.write(f"Error: CSV file '{args.csv_path}' not found.\n")
        return 1

    try:
        tasks = load_tasks(csv_file)
    except (OSError, ValueError, KeyError) as exc:
        sys.stderr.write(f"Error loading tasks: {exc}\n")
        return 1

    allocated = allocate_tasks(tasks, args.hours, args.today)
    print(format_plan(allocated, args.hours))
    return 0


if __name__ == "__main__":
    sys.exit(main())
