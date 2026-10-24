import argparse
import sys
from collections.abc import Sequence
from datetime import date

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render


def run(csv_path: str, hours: float, today: date) -> str:
    """Build the plan text for ``csv_path`` with ``hours`` available on ``today``."""
    tasks = parse_csv(csv_path)
    ordered = prioritise(tasks, today)
    blocks = allocate(ordered, hours)
    return render(blocks)


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
        prog="python -m shared.study_planner",
        description="Turn a tasks CSV into a study plan for the hours you have.",
    )
    parser.add_argument(
        "csv_path", help="CSV with header title,importance,effort_h,deadline"
    )
    parser.add_argument(
        "--hours", type=float, required=True, help="study hours available"
    )
    parser.add_argument(
        "--today",
        type=parse_iso_date,
        default=None,
        help="today's date, YYYY-MM-DD (default: the real date; use it for reproducible output)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return the exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.hours <= 0:
        parser.error("--hours must be greater than 0")

    # Member 3 (T-W3 step 3): wrap this call with error handling
    # (missing file, empty file, InfeasiblePlan).
    print(run(args.csv_path, args.hours, args.today or date.today()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
