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

├── docs/
│   └── demo.md          # Demo execution logs & scenario proofs
├── shared/              # Shared team code directory
│   ├── contract.py      # Data models & contract definitions
│   └── study_planner/   # Study Planner core module
│       ├── README.md    # Application documentation & CLI guide
│       ├── __main__.py  # CLI entry point & execution flow
│       ├── allocate.py  # Time slot allocation logic
│       ├── parse.py     # CSV task parser module
│       ├── prioritise.py# Task sorting & priority calculator
│       ├── render.py    # Console schedule renderer
│       └── validate.py  # Feasibility & constraint validator
└── tests/               # Integration & E2E test scripts