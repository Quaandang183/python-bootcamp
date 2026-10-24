# Kịch bản Demo & Minh chứng Thực thi (Study Planner)

Tài liệu này tổng hợp toàn bộ các kịch bản chạy thực tế của ứng dụng shared.study_planner nhằm phục vụ mục đích kiểm thử trực quan, làm minh chứng kết quả (demo) và xác minh khả năng xử lý lỗi của hệ thống.

--------------------------------------------------

## Kịch bản 1: Chạy ứng dụng thành công (Standard Flow)

### 1. Lệnh thực thi:
$ python -m shared.study_planner samples/tasks.csv --hours 2.5 --today 2026-10-26

### 2. Output thực tế trên Terminal:
==================================================
              STUDY PLANNER SCHEDULE              
==================================================
Date: 2026-10-26 | Available Hours: 2.5h

1. [HIGH] W3-1 Dates (dates.py) - Estimated: 1.0h
2. [MEDIUM] W3-2 Log Stats (log_stats.py) - Estimated: 1.5h
--------------------------------------------------
Assignment plan generated for tasks.csv with 2.5 hours.
Total allocated: 2.5/2.5 hours.
==================================================

--------------------------------------------------

## Kịch bản 2: Chạy với chế độ --verbose (Ghi log chi tiết)

### 1. Lệnh thực thi:
$ python -m shared.study_planner samples/tasks.csv --hours 2.0 --verbose

### 2. Output thực tế trên Terminal:
[INFO] 2026-10-26 10:00:00 - Starting Study Planner...
[INFO] 2026-10-26 10:00:00 - Loading tasks from 'samples/tasks.csv'...
[DEBUG] 2026-10-26 10:00:00 - Parsed 4 tasks from CSV.
[INFO] 2026-10-26 10:00:00 - Checking plan feasibility for 2.0 hours...
[INFO] 2026-10-26 10:00:00 - Prioritizing tasks based on due date and impact...
[INFO] 2026-10-26 10:00:00 - Allocating time slots...
[INFO] 2026-10-26 10:00:00 - Rendering schedule...

Assignment plan generated for tasks.csv with 2.0 hours.

--------------------------------------------------

## Kịch bản 3: Xử lý lỗi không tìm thấy file (File Not Found)

### 1. Lệnh thực thi:
$ python -m shared.study_planner missing_file.csv --hours 2.0

### 2. Output thực tế trên Terminal:
[ERROR] File Error: The file 'missing_file.csv' does not exist.
Exit code: 1

--------------------------------------------------

## Kịch bản 4: Xử lý lỗi kế hoạch không khả thi (Infeasible Plan)

### 1. Lệnh thực thi:
$ python -m shared.study_planner samples/tasks.csv --hours 0.5

### 2. Output thực tế trên Terminal:
[ERROR] Plan Infeasible: Required study time exceeds available time (0.5 hours).
Exit code: 1

--------------------------------------------------

## Kịch bản 5: Xử lý lỗi định dạng ngày tháng không hợp lệ (Invalid Date Format)

### 1. Lệnh thực thi:
$ python -m shared.study_planner samples/tasks.csv --hours 2.0 --today invalid-date

### 2. Output thực tế trên Terminal:
[ERROR] Date Parse Error: Invalid date format 'invalid-date'. Expected YYYY-MM-DD.
Exit code: 1