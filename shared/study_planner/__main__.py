import argparse
import sys
from collections.abc import Sequence
from datetime import date

from .allocate import allocate
from .parse import parse_csv
from .prioritise import prioritise
from .render import render
from .validate import InfeasiblePlan, check_feasible

EXIT_OK = 0
EXIT_ERROR = 1


class EmptyTasksFile(Exception):
    """The CSV file has no task rows (empty file or header only)."""


def run(csv_path: str, hours: float, today: date) -> str:
    """Run the whole pipeline and return the plan as text.

    Raises FileNotFoundError, OSError, ValueError (bad row or date),
    EmptyTasksFile and InfeasiblePlan; main() turns them into messages.
    """
    tasks = parse_csv(csv_path)
    if not tasks:
        raise EmptyTasksFile(csv_path)
    check_feasible(tasks, hours)
    ordered = prioritise(tasks, today)
    blocks = allocate(ordered, hours)
    return render(blocks)


def fail(message: str) -> int:
    """Print a friendly error message to stderr and return the error exit code."""
    print(f"Lỗi: {message}", file=sys.stderr)
    return EXIT_ERROR


def main(argv: Sequence[str] | None = None) -> int:
    """Read the command line, print the plan and return the exit code."""
    parser = argparse.ArgumentParser(prog="python -m shared.study_planner")
    parser.add_argument("csv_path", help="CSV with header title,importance,effort_h,deadline")
    parser.add_argument("--hours", type=float, required=True, help="study hours available")
    args = parser.parse_args(argv)

    try:
        plan = run(args.csv_path, args.hours, date.today())
    except FileNotFoundError:
        return fail(f"không tìm thấy file '{args.csv_path}'. Hãy kiểm tra lại đường dẫn.")
    except EmptyTasksFile:
        return fail(f"file '{args.csv_path}' không có nhiệm vụ nào (file rỗng hoặc chỉ có dòng tiêu đề).")
    except InfeasiblePlan as exc:
        return fail(f"{exc}\n      Hãy tăng --hours hoặc bớt nhiệm vụ trong file.")
    except ValueError as exc:  # bad number, bad date (YYYY-MM-DD expected) or wrong columns
        return fail(
            f"dữ liệu trong '{args.csv_path}' không hợp lệ: {exc}\n"
            "      Cần: importance là số nguyên, effort_h là số, deadline có dạng YYYY-MM-DD."
        )
    except OSError as exc:  # a folder, no permission, ...
        return fail(f"không đọc được '{args.csv_path}': {exc.strerror or exc}")

    print(plan)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
