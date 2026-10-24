"""W3-3: command-line study planner.

Run with:
    python -m members.Quaandang183.w3.cli tasks.csv --hours 2 --today 2026-10-26
"""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from ..w2.io_utils import load_tasks
from ..w2.models import Task


def prioritise(tasks: list[Task], today: date) -> list[Task]:
    """Order tasks by importance divided by days left (most urgent first)."""
    return sorted(
        tasks,
        key=lambda t: (-t.importance / max(t.days_left(today), 1), t.deadline, t.title),
    )


def allocate(tasks: list[Task], hours: float) -> list[tuple[Task, float]]:
    """Give each task up to its effort, in order, until the hours run out."""
    blocks: list[tuple[Task, float]] = []
    remaining = hours
    for task in tasks:
        if remaining <= 0:
            break
        spent = min(task.effort_h, remaining)
        blocks.append((task, spent))
        remaining -= spent
    return blocks


def render(blocks: list[tuple[Task, float]], hours: float) -> str:
    """Format the plan as a numbered list with dotted leaders."""
    lines = [f"Tonight ({hours:.1f} h):"]
    if not blocks:
        lines.append("  Nothing to do.")
        return "\n".join(lines)
    width = max(len(task.title) for task, _ in blocks) + 7
    for i, (task, spent) in enumerate(blocks, start=1):
        label = f"{task.title} ".ljust(width, ".")
        lines.append(f"  {i}. {label} {spent:.1f} h")
    return "\n".join(lines)


def parse_iso_date(text: str) -> date:
    """Argparse type for ``--today YYYY-MM-DD``."""
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"not a valid YYYY-MM-DD date: {text!r}"
        ) from exc


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="cli", description="Plan tonight's study hours from a tasks CSV."
    )
    parser.add_argument(
        "csv_path", type=Path, help="CSV: title,importance,effort_h,deadline"
    )
    parser.add_argument(
        "--hours", type=float, required=True, help="hours available tonight"
    )
    parser.add_argument(
        "--today",
        type=parse_iso_date,
        default=None,
        help="today's date, YYYY-MM-DD (default: the real date)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return the exit code (1 for a missing or invalid file)."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.hours <= 0:
        parser.error("--hours must be greater than 0")
    today = args.today or date.today()

    try:
        tasks = load_tasks(args.csv_path)
    except FileNotFoundError:
        print(f"error: file not found: {args.csv_path}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"error: invalid tasks file {args.csv_path}: {exc}", file=sys.stderr)
        return 1

    print(render(allocate(prioritise(tasks, today), args.hours), args.hours))
    return 0


if __name__ == "__main__":
    sys.exit(main())
