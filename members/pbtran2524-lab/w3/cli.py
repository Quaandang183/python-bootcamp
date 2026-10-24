import argparse
import sys
from datetime import date, datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Task CLI Tool")
    parser.add_argument("file", type=Path, help="Path to tasks CSV file")
    parser.add_argument("--hours", type=float, default=None, help="Available hours")
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Date in YYYY-MM-DD format (default: today)"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # Kiểm tra sự tồn tại của tệp
    if not args.file.is_file():
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Đọc và xử lý danh sách công việc (Tái sử dụng logic từ W2 của bạn)
    # Ví dụ minh họa hiển thị:
    print(f"Tonight ({args.hours or 0.0} h):")
    # ... In danh sách công việc theo tham số args.today và args.hours ...

if __name__ == "__main__":
    main()