# Demo Scenarios and Execution Proofs (Study Planner)

This document collects real-world execution scenarios for the shared.study_planner application using the provided tasks.csv and tasks_bad.csv datasets. It serves as visual testing, proof of output, and verification of top-level error handling.

--------------------------------------------------

## Scenario 1: Standard Execution (Success Flow)

### 1. Command Line:
$ python -m shared.study_planner tasks.csv --hours 8.0 --today 2026-10-26

### 2. Actual Terminal Output (stdout):
=== STUDY PLAN ===
1. Assignment | Allocated: 1.5h / 1.5h | Importance: 4
2. DS exam | Allocated: 6.0h / 6.0h | Importance: 5
--------------------------------
Total study time: 7.5h

--------------------------------------------------

## Scenario 2: Execution with Verbose Logging (-v / --verbose)

### 1. Command Line:
$ python -m shared.study_planner tasks.csv --hours 8.0 --today 2026-10-26 -v

### 2. Actual Terminal Output:
INFO: Đã đọc thành công 2 nhiệm vụ từ file tasks.csv
INFO: Quỹ thời gian 8h là khả thi (cần 7.5h)
INFO: Đã sắp xếp 2 nhiệm vụ theo độ ưu tiên (tính từ 2026-10-26)
INFO: Đã chia 2 khối thời gian, tổng 7.5h
=== STUDY PLAN ===
1. Assignment | Allocated: 1.5h / 1.5h | Importance: 4
2. DS exam | Allocated: 6.0h / 6.0h | Importance: 5
--------------------------------
Total study time: 7.5h

--------------------------------------------------

## Scenario 3: Error Handling - Infeasible Plan (Insufficient Time)

### 1. Command Line:
$ python -m shared.study_planner tasks.csv --hours 3.0 --today 2026-10-26

### 2. Actual Terminal Output (stderr):
Lỗi: Kế hoạch không khả thi: Cần 7.5h nhưng chỉ có 3.0h khả dụng.
      Hãy tăng --hours hoặc bớt nhiệm vụ trong file.

--------------------------------------------------

## Scenario 4: Error Handling - File Not Found

### 1. Command Line:
$ python -m shared.study_planner missing.csv --hours 5.0

### 2. Actual Terminal Output (stderr):
Lỗi: không tìm thấy file 'missing.csv'. Hãy kiểm tra lại đường dẫn.

--------------------------------------------------

## Scenario 5: Error Handling - Invalid CSV Data Row (tasks_bad.csv)

### 1. Command Line:
$ python -m shared.study_planner tasks_bad.csv --hours 5.0

### 2. Actual Terminal Output (stderr):
Lỗi: Kế hoạch không khả thi: Cần 7.0h nhưng chỉ có 5.0h khả dụng.
      Hãy tăng --hours hoặc bớt nhiệm vụ trong file.

--------------------------------------------------

## Scenario 6: Error Handling - Invalid Command Line Date Format

### 1. Command Line:
$ python -m shared.study_planner tasks.csv --hours 5.0 --today 26-10-2026

### 2. Actual Terminal Output (stderr):
usage: python -m shared.study_planner [-h] --hours HOURS [--today TODAY] [-v] csv_path
python -m shared.study_planner: error: argument --today: '26-10-2026' không phải ngày hợp lệ, cần dạng YYYY-MM-DD