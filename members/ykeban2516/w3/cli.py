"""Read a task CSV and print a plan within the available study hours."""

import argparse
import logging
from collections.abc import Sequence
from datetime import date
from math import isfinite

from ..w2.io_utils import load_tasks

LOGGER = logging.getLogger(__name__)


def positive_hours(value: str) -> float:
    """Validate a finite, positive hour budget for argparse.

    Args:
        value: String representation of hour budget.

    Returns:
        Validated float hour value.

    Raises:
        argparse.ArgumentTypeError: If value is non-numeric, non-finite, or <= 0.
    """
    try:
        hours = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Hours must be a number") from error
    if not isfinite(hours) or hours <= 0:
        raise argparse.ArgumentTypeError("Hours must be finite and positive")
    return hours


def main(argv: Sequence[str] | None = None) -> int:
    """Execute study planner CLI to load tasks and generate a prioritized plan.

    Args:
        argv: Command-line argument sequence, or None for sys.argv[1:].

    Returns:
        0 on success, or 1 if input file or task data is invalid.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    parser.add_argument("--hours", required=True, type=positive_hours)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    try:
        tasks = load_tasks(args.csv_path)
        if not tasks:
            raise ValueError("CSV contains no tasks")
    except (OSError, ValueError) as error:
        LOGGER.error("Cannot load tasks: %s", error)
        return 1

    LOGGER.debug("Loaded %d tasks", len(tasks))
    ordered = sorted(
        tasks,
        key=lambda task: task.importance / max(task.days_left(args.today), 1),
        reverse=True,
    )

    remaining = args.hours
    print(f"Study plan for {args.today.isoformat()}")
    for task in ordered:
        if remaining <= 0:
            break
        allocated = min(task.effort_h, remaining)
        if allocated <= 0:
            continue
        print(f"{task.title}: {allocated:g}h | deadline {task.deadline.isoformat()}")
        remaining -= allocated

    print(f"Total: {args.hours - remaining:g}h / {args.hours:g}h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
