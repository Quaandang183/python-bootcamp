from datetime import date
from pathlib import Path
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from .models import Task
    from .io_utils import load_tasks, save_json
    from .errors import InfeasiblePlan, check_feasible
except ImportError:
    from models import Task
    from io_utils import load_tasks, save_json
    from errors import InfeasiblePlan, check_feasible


def main():
    current_dir = Path(__file__).resolve().parent
    csv_path = current_dir / "tasks.csv"
    if not csv_path.exists():
        sample_path = current_dir.parents[2] / "samples" / "tasks.csv"
        if sample_path.exists():
            csv_path = sample_path

    print("=" * 60)
    print("=== DEMO CHUONG TRINH QUAN LY NHIEM VU (W2 PACKAGE) ===")
    print("=" * 60)

    if not csv_path.exists():
        print(f"Khong tim thay file {csv_path.name} de doc du lieu mau!")
        return

    print(f"\n[1] Dang nap danh sach nhiem vu tu file: {csv_path.name}...")
    try:
        tasks = load_tasks(csv_path)
        print(f"-> Nap thanh cong {len(tasks)} nhiem vu!\n")
    except ValueError as e:
        print(f"Loi khi doc file CSV: {e}")
        return

    today = date(2026, 10, 26)
    print(f"--- DANH SACH NHIEM VU (Ngay hien tai gia dinh: {today}) ---")
    print(f"{'STT':<4} | {'Ten nhiem vu':<22} | {'Quan trong':<10} | {'Thoi luong':<10} | {'Han chot':<12} | {'Con lai'}")
    print("-" * 80)
    for idx, t in enumerate(tasks, start=1):
        remaining = t.days_left(today)
        print(f"{idx:<4} | {t.title:<22} | {t.importance:<10} | {t.duration:<10.1f} | {str(t.deadline):<12} | {remaining} ngay")
    print("-" * 80)

    # Kiem tra tinh kha thi
    available_hours = 15.0
    print(f"\n[2] Kiem tra tinh kha thi voi so gio kha dung = {available_hours}h:")
    try:
        check_feasible(tasks, available_hours)
        total_h = sum(t.duration for t in tasks)
        print(f"-> Ke hoach hoan toan KHA THI (Tong gio: {total_h}h <= {available_hours}h).")
    except InfeasiblePlan as err:
        print(f"-> Canh bao: {err}")

    # Xuat ra file JSON
    out_json = current_dir / "tasks_output.json"
    save_json(tasks, out_json)
    print(f"\n[3] Da luu danh sach nhiem vu ra file JSON: {out_json.name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
