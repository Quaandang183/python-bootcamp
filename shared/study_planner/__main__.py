import argparse
import logging
import sys
from datetime import date, datetime
from pathlib import Path

# Import các module từ Tuần 2
from shared.study_planner.allocate import allocate
from shared.study_planner.check_feasible import check_feasible
from shared.study_planner.parse_csv import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render


def setup_logging(verbose: bool) -> None:
    """Cấu hình hệ thống logging dựa trên cờ --verbose."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """Thiết lập và phân tích các tham số dòng lệnh (CLI)."""
    parser = argparse.ArgumentParser(
        description="Study Planner CLI - Công cụ lập kế hoạch học tập tự động"
    )

    # Tham số bắt buộc: Đường dẫn file CSV
    parser.add_argument(
        "file",
        type=Path,
        help="Đường dẫn tới file tasks.csv chứa danh sách công việc",
    )

    # Tham số tùy chọn: Quỹ thời gian khả dụng (giờ)
    parser.add_argument(
        "--hours",
        type=float,
        default=None,
        help="Số giờ học khả dụng (ví dụ: --hours 2.0)",
    )

    # Tham số tùy chọn: Ngày mốc tính toán (mặc định là hôm nay)
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Ngày mốc tính toán định dạng YYYY-MM-DD (mặc định: hôm nay)",
    )

    # Tham số tùy chọn: Bật ghi log chi tiết
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Bật chế độ ghi log chi tiết (DEBUG mode)",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)

    logging.debug("Bắt đầu khởi chạy Study Planner...")
    logging.debug(f"Tham số nhận vào: file={args.file}, hours={args.hours}, today={args.today}")

    # Bọc try...except để xử lý ngoại lệ (Phần việc phối hợp với Thành viên 3)
    try:
        # 1. Đọc dữ liệu từ file CSV
        if not args.file.is_file():
            raise FileNotFoundError(f"Không tìm thấy file: {args.file}")
        
        logging.info(f"Đang đọc dữ liệu từ {args.file}...")
        tasks = parse_csv(args.file)

        # 2. Kiểm tra tính khả thi của thời gian
        logging.info("Đang kiểm tra quỹ thời gian...")
        check_feasible(tasks, available_hours=args.hours)

        # 3. Sắp xếp thứ tự ưu tiên
        logging.info("Đang sắp xếp thứ tự ưu tiên các công việc...")
        prioritised_tasks = prioritise(tasks, today=args.today)

        # 4. Phân bổ khối thời gian
        logging.info("Đang phân bổ thời gian cho các công việc...")
        schedule = allocate(prioritised_tasks, available_hours=args.hours)

        # 5. Xuất chuỗi văn bản kết quả
        logging.info("Hoàn tất lập kế hoạch. Đang xuất kết quả:")
        output_text = render(schedule, available_hours=args.hours)
        
        # In kết quả ra màn hình cho người dùng
        print(output_text)

    except FileNotFoundError as e:
        logging.error(f"Lỗi tệp tin: {e}")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"Lỗi dữ liệu / Định dạng ngày tháng: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Đã xảy ra lỗi không xác định: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()