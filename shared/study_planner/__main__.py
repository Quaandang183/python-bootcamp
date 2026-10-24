import argparse
import sys
from collections.abc import Sequence
from datetime import date

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render
from .validate import check_feasible


def run(csv_path: str, hours: float, today: date) -> str:
    """Run the whole pipeline and return the plan as text."""
    tasks = parse_csv(csv_path)  # 1. read the tasks
    check_feasible(tasks, hours)  # 2. do we have enough hours?
    ordered = prioritise(tasks, today)  # 3. most urgent first
    blocks = allocate(ordered, hours)  # 4. split the available hours
    return render(blocks)  # 5. build the output text


def main(argv: Sequence[str] | None = None) -> int:
    """Read the command line, print the plan and return the exit code."""
    parser = argparse.ArgumentParser(prog="python -m shared.study_planner")
    parser.add_argument("csv_path", help="CSV with header title,importance,effort_h,deadline")
    parser.add_argument("--hours", type=float, required=True, help="study hours available")
    args = parser.parse_args(argv)

    print(run(args.csv_path, args.hours, date.today()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
