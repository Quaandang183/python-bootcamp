import argparse
import logging
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

log = logging.getLogger("study_planner")


class EmptyTasksFile(Exception):
    """The CSV file has no task rows (empty file or header only)."""


def setup_logging(verbosity: int) -> None:
    """Configure logging on stderr: WARNING by default, INFO for -v, DEBUG for -vv."""
    level = (logging.WARNING, logging.INFO, logging.DEBUG)[min(verbosity, 2)]
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr, force=True)


def parse_iso_date(text: str) -> date:
    """Argparse type for ``--today``: a date written YYYY-MM-DD."""
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"'{text}' không phải ngày hợp lệ, cần dạng YYYY-MM-DD") from exc


def positive_hours(text: str) -> float:
    """Argparse type for ``--hours``: a number greater than 0."""
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"'{text}' không phải là số giờ") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("số giờ phải lớn hơn 0")
    return value


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="python -m shared.study_planner",
        description="Chia quỹ thời gian học cho các nhiệm vụ trong file CSV.",
    )
    parser.add_argument("csv_path", help="CSV with header title,importance,effort_h,deadline")
    parser.add_argument("--hours", type=positive_hours, required=True, help="số giờ học có sẵn")
    parser.add_argument(
        "--today",
        type=parse_iso_date,
        default=None,
        help="ngày hôm nay, YYYY-MM-DD (mặc định: ngày thật; dùng để kết quả lặp lại được)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="in các bước chi tiết ra stderr (-vv: thêm thông tin DEBUG)",
    )
    return parser


def run(csv_path: str, hours: float, today: date) -> str:
    """Run the whole pipeline and return the plan as text.

    Raises FileNotFoundError, OSError, ValueError (bad row or date),
    EmptyTasksFile and InfeasiblePlan; main() turns them into messages.
    """
    log.debug("Bắt đầu: file=%s, hours=%g, today=%s", csv_path, hours, today)

    tasks = parse_csv(csv_path)
    if not tasks:
        raise EmptyTasksFile(csv_path)
    log.info("Đã đọc thành công %d nhiệm vụ từ file %s", len(tasks), csv_path)

    check_feasible(tasks, hours)
    needed = sum(t.effort_h for t in tasks)
    log.info("Quỹ thời gian %gh là khả thi (cần %gh)", hours, needed)

    ordered = prioritise(tasks, today)
    log.info("Đã sắp xếp %d nhiệm vụ theo độ ưu tiên (tính từ %s)", len(ordered), today)
    for rank, task in enumerate(ordered, start=1):
        log.debug("  #%d %s (importance %d, hạn %s)", rank, task.title, task.importance, task.deadline)

    blocks = allocate(ordered, hours)
    log.info("Đã chia %d khối thời gian, tổng %gh", len(blocks), sum(b.hours for b in blocks))

    return render(blocks)


def fail(message: str) -> int:
    """Print a friendly error message to stderr and return the error exit code."""
    print(f"Lỗi: {message}", file=sys.stderr)
    return EXIT_ERROR


def main(argv: Sequence[str] | None = None) -> int:
    """Read the command line, print the plan and return the exit code."""
    args = build_parser().parse_args(argv)
    setup_logging(args.verbose)
    today = args.today or date.today()

    try:
        plan = run(args.csv_path, args.hours, today)
    except FileNotFoundError:
        log.debug("chi tiết lỗi", exc_info=True)
        return fail(f"không tìm thấy file '{args.csv_path}'. Hãy kiểm tra lại đường dẫn.")
    except EmptyTasksFile:
        return fail(f"file '{args.csv_path}' không có nhiệm vụ nào (file rỗng hoặc chỉ có dòng tiêu đề).")
    except InfeasiblePlan as exc:
        return fail(f"{exc}\n      Hãy tăng --hours hoặc bớt nhiệm vụ trong file.")
    except ValueError as exc:  # bad number, bad date (YYYY-MM-DD expected) or wrong columns
        log.debug("chi tiết lỗi", exc_info=True)
        return fail(
            f"dữ liệu trong '{args.csv_path}' không hợp lệ: {exc}\n"
            "      Cần: importance là số nguyên, effort_h là số, deadline có dạng YYYY-MM-DD."
        )
    except OSError as exc:  # a folder, no permission, ...
        log.debug("chi tiết lỗi", exc_info=True)
        return fail(f"không đọc được '{args.csv_path}': {exc.strerror or exc}")

    print(plan)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
