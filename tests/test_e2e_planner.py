
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED_DIR = REPO_ROOT / "shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.validate import check_feasible

SAMPLE_CSV = REPO_ROOT / "samples" / "tasks.csv"
ENV = {
    **os.environ,
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUTF8": "1",
    "PYTHONPATH": f"{REPO_ROOT}{os.pathsep}{SHARED_DIR}{os.pathsep}{os.environ.get('PYTHONPATH', '')}".rstrip(os.pathsep),
}


def test_e2e_cli_valid_schedule(tmp_path: Path) -> None:
    """Test CLI execution with a feasible schedule (hours >= total needed effort).

    Verifies that the process exits with code 0 without crashing and
    produces the expected schedule.
    """
    csv_file = tmp_path / "valid_tasks.csv"
    csv_file.write_text(
        "title,importance,effort_h,deadline\n"
        "Assignment,4,1.5,2026-10-27\n"
        "Quiz,3,0.5,2026-10-28\n",
        encoding="utf-8",
    )

    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(csv_file),
        "--hours",
        "2",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 0, f"Process crashed with error: {result.stderr}"
    assert "STUDY PLAN" in result.stdout
    assert "Assignment" in result.stdout
    assert "Quiz" in result.stdout
    assert "2.0h" in result.stdout


def test_e2e_cli_sample_csv_with_sufficient_hours() -> None:
    """Test CLI execution using the repository samples/tasks.csv with sufficient hours."""
    assert SAMPLE_CSV.is_file(), f"Sample file not found at: {SAMPLE_CSV}"

    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(SAMPLE_CSV),
        "--hours",
        "8",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 0, f"Process crashed with error: {result.stderr}"
    assert "STUDY PLAN" in result.stdout
    assert "Assignment" in result.stdout
    assert "DS exam" in result.stdout


def test_e2e_cli_infeasible_plan() -> None:
    """Test CLI execution when total effort exceeds available hours.

    Member 3 requirement: InfeasiblePlan should be handled gracefully and return code 1.
    """
    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(SAMPLE_CSV),
        "--hours",
        "2",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 1
    combined = (result.stdout or "") + (result.stderr or "")
    assert "7.5h" in combined or "--hours" in combined or "thi" in combined


def test_e2e_cli_with_today_option(tmp_path: Path) -> None:
    """Test CLI execution specifying --today option.

    Ensures tasks are ordered by urgency relative to the given reference date.
    """
    csv_file = tmp_path / "tasks.csv"
    csv_file.write_text(
        "title,importance,effort_h,deadline\n"
        "Later Task,5,1.0,2026-10-30\n"
        "Urgent Task,4,1.0,2026-10-27\n",
        encoding="utf-8",
    )

    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(csv_file),
        "--hours",
        "2",
        "--today",
        "2026-10-26",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 0
    pos_urgent = result.stdout.find("Urgent Task")
    pos_later = result.stdout.find("Later Task")
    assert pos_urgent != -1 and pos_later != -1
    assert pos_urgent < pos_later, "Urgent Task should be prioritised before Later Task"


def test_e2e_cli_verbose_logging(tmp_path: Path) -> None:
    """Test CLI execution with verbose logging flag enabled."""
    csv_file = tmp_path / "tasks.csv"
    csv_file.write_text(
        "title,importance,effort_h,deadline\n"
        "Task A,5,1.0,2026-10-30\n",
        encoding="utf-8",
    )

    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(csv_file),
        "--hours",
        "2",
        "-v",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 0
    combined = (result.stdout or "") + (result.stderr or "")
    assert "INFO" in combined or "DEBUG" in combined


def test_e2e_cli_missing_file() -> None:
    """Test CLI behavior when the input CSV file does not exist."""
    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        "nonexistent_tasks.csv",
        "--hours",
        "2",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 1
    combined = (result.stdout or "") + (result.stderr or "")
    assert "nonexistent_tasks.csv" in combined


def test_e2e_cli_empty_file(tmp_path: Path) -> None:
    """Test CLI behavior when the input CSV file is empty."""
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("title,importance,effort_h,deadline\n", encoding="utf-8")

    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(empty_csv),
        "--hours",
        "2",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode == 1
    combined = (result.stdout or "") + (result.stderr or "")
    assert str(empty_csv.name) in combined or "empty" in combined.lower()


def test_e2e_cli_missing_required_hours() -> None:
    """Test CLI behavior when the required --hours argument is omitted."""
    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(SAMPLE_CSV),
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        errors="replace",
        env=ENV,
        check=False,
    )

    assert result.returncode != 0


def test_pipeline_programmatic_flow() -> None:
    """Test programmatic integration of the 5 submodules from start to finish."""
    # 1. Parse
    tasks = parse_csv(str(SAMPLE_CSV))
    assert len(tasks) >= 2

    # 2. Feasibility check
    check_feasible(tasks, available_h=10.0)

    # 3. Prioritise
    today = date(2026, 10, 26)
    ordered = prioritise(tasks, today=today)
    assert ordered[0].title == "Assignment"

    # 4. Allocate
    blocks = allocate(ordered, hours=2.0)
    assert len(blocks) == 2
    assert blocks[0].hours == 1.5
    assert blocks[1].hours == 0.5

    # 5. Render
    rendered = render(blocks)
    assert "=== STUDY PLAN ===" in rendered
    assert "Total study time" in rendered
