import argparse
import csv
import logging
import sys
from datetime import date, datetime
from math import isfinite
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.validate import InfeasiblePlan, check_feasible


def setup_logging(verbose: bool) -> None:
    """Configure logging according to the verbose flag."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Study Planner CLI - Cong cu lap ke hoach hoc tap"
    )
    parser.add_argument("file", type=Path, help="Duong dan toi file tasks.csv")
    parser.add_argument(
        "--hours", type=float, default=None, help="So gio hoc kha dung"
    )
    parser.add_argument(
        "--today",
        type=lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        default=date.today(),
        help="Ngay moc YYYY-MM-DD (mac dinh: hom nay)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Bat ghi log chi tiet"
    )
    return parser.parse_args()


def main() -> None:
    """Run the planner and report expected input errors."""
    args = parse_args()
    setup_logging(args.verbose)

    if args.hours is None or not isfinite(args.hours) or args.hours <= 0:
        logging.error("Hay nhap --hours la so huu han lon hon 0.")
        sys.exit(2)

    logging.debug("Bat dau khoi chay Study Planner...")
    logging.debug(
        "Tham so: file=%s, hours=%s, today=%s",
        args.file, args.hours, args.today,
    )

    try:
        logging.info("Dang doc du lieu tu %s...", args.file)
        tasks = parse_csv(args.file)

        if not tasks:
            raise ValueError("File CSV rong hoac khong co nhiem vu.")

        logging.info("Dang kiem tra quy thoi gian...")
        check_feasible(tasks, args.hours)

        logging.info("Dang sap xep thu tu uu tien cac cong viec...")
        prioritised_tasks = prioritise(tasks, today=args.today)

        logging.info("Dang phan bo thoi gian cho cac cong viec...")
        schedule = allocate(prioritised_tasks, args.hours)

        from shared.study_planner.render import render

        logging.info("Hoan tat lap ke hoach. Dang xuat ket qua:")
        output_text = render(schedule)
        print(output_text)

    except FileNotFoundError:
        logging.error("Khong tim thay file: %s", args.file)
        sys.exit(1)
    except PermissionError:
        logging.error("Khong co quyen doc file: %s", args.file)
        sys.exit(1)
    except InfeasiblePlan as error:
        logging.error(
            "Ke hoach khong kha thi: can %gh, nhung chi co %gh.",
            error.needed_h, error.available_h,
        )
        sys.exit(1)
    except UnicodeError:
        logging.error("Khong doc duoc ma hoa file. Hay luu CSV bang UTF-8.")
        sys.exit(1)
    except (ValueError, csv.Error) as error:
        logging.error("Du lieu CSV hoac ngay thang khong hop le: %s", error)
        sys.exit(1)
    except OSError as error:
        logging.error("Khong doc duoc file: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
