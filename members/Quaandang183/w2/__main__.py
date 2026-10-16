"""Run using: python -m members.Quaandang183.w2 [csv_path]

Reads a sample CSV file (default: python-bootcamp/samples/tasks.csv) and prints the tasks.
"""
import sys
from datetime import date
from pathlib import Path

from .io_utils import load_tasks

DEFAULT_CSV = Path(__file__).resolve().parents[3] / "samples" / "tasks.csv"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    path = Path(args[0]) if args else DEFAULT_CSV
    try:
        tasks = load_tasks(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error in {path.name}: {e}", file=sys.stderr)
        return 1

    today = date.today()
    print(f"Loaded {len(tasks)} task(s) from {path.name}:")
    for i, t in enumerate(tasks, start=1):
        print(
            f"{i}. {t.title} | importance {t.importance} | {t.effort_h:g}h "
            f"| due {t.deadline.isoformat()} ({t.days_left(today)} day(s) left)"
        )
    print(f"Total effort: {sum(t.effort_h for t in tasks):g}h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
