# Python Bootcamp (Week 1 - Week 3)
This directory contains the group's Python warm-up exercises for the first three weeks. The goal is to become familiar with Python syntax, data structures, and collaborative workflows using Git/GitHub.

## Directory Structure
* `members/`: Contains individual exercise source code. **Rule:** Each member must write code only in their own directory (`members/<github_username>/`). Directory names must use underscores (`_`) instead of hyphens (`-`).
* `shared/`: Contains code shared by the entire group for group assignments T-W2 and T-W3.
* `tests/`: Contains unit test files (`pytest`) provided by the instructor for automated grading.

## How to Run Tests
The group uses `pytest` to verify code correctness. The `conftest.py` file is configured to automatically load code from your personal directory.
Open a Terminal (or Git Bash), navigate to the repository root directory, and run the following command:

```bash
pytest -q python-bootcamp/tests/test_w1.py --member <your_directory_name> --variant <number_from_1_to_4>
```
