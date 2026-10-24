# Study Planner CLI Application

Ứng dụng lập kế hoạch học tập tự động qua giao diện dòng lệnh (CLI). Công cụ giúp người dùng phân tích danh sách bài tập, kiểm tra tính khả thi dựa trên quỹ thời gian, tự động sắp xếp thứ tự ưu tiên và phân bổ khối thời gian học tập hợp lý.

---

## 1. Tính năng chính

* **Đọc & Phân tích (Parse):** Đọc dữ liệu công việc từ file CSV.
* **Kiểm tra khả thi (Feasibility Check):** Tính toán và cảnh báo nếu tổng thời gian bài tập vượt quá quỹ thời gian khả dụng.
* **Ưu tiên công việc (Prioritization):** Sắp xếp thứ tự ưu tiên dựa trên hạn chót (due date) và mức độ quan trọng.
* **Phân bổ thời gian (Time Allocation):** Chia nhỏ khối thời gian học tập phù hợp theo mục tiêu trong ngày.
* **Xuất kết quả (Render):** Hiển thị lịch trình trực quan, dễ theo dõi trên Terminal.
* **Nhật ký hệ thống (Logging):** Hỗ trợ chế độ `--verbose` giúp theo dõi luồng xử lý chi tiết.

---

## 2. Cấu trúc thư mục dự án

```text
shared/
└── study_planner/
    ├── __init__.py
    ├── __main__.py          # Luồng chạy chính (Quân, Trân, Khanh)
    └── README.md            # Tài liệu hướng dẫn (Oanh)
docs/
└── demo.md                  # Kịch bản và minh chứng chạy demo (Oanh)
tests/
└── test_e2e_planner.py      # Kịch bản kiểm thử End-to-End (Bảo)