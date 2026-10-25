# Study Planner CLI Application

An automated command-line interface (CLI) application designed to generate study schedules. The tool parses task lists, verifies schedule feasibility against available study hours, prioritizes tasks based on deadlines and importance, allocates time slots, and renders a formatted output.

---

## 1. Key Features

* **Parsing:** Read and extract task metadata from standard CSV files.
* **Feasibility Check:** Calculate total estimated time and issue warnings if total work exceeds available daily hours.
* **Prioritization:** Dynamically sort tasks based on due dates and impact ratings.
* **Time Allocation:** Divide available time slots efficiently to optimize study productivity.
* **Rendering:** Display a clean, human-readable terminal schedule.
* **Logging & Debugging:** Provide a `--verbose` flag for step-by-step runtime execution logs.

---

## 2. Directory Structure

```text
shared/
└── study_planner/
    ├── __init__.py
    ├── __main__.py          # Main execution flow (Quân, Trân, Khanh)
    └── README.md            # Technical documentation (Oanh)
docs/
└── demo.md                  # Demo execution logs & proof of test (Oanh)
tests/
└── test_e2e_planner.py      # End-to-End integration tests (Bảo)