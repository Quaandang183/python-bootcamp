"""End-to-end integration test suite for the shared study planner CLI.

Author: NgoGiaBao279 (TV2 - E2E Tester)
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.validate import check_feasible

REPO_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_CSV = REPO_ROOT / "samples" / "tasks.csv"


def test_e2e_cli_valid_sample() -> None:
    """Test CLI execution with a valid sample CSV and --hours 2.

    Verifies that the process exits with code 0 without crashing and
    produces the expected schedule.
    """
    assert SAMPLE_CSV.is_file(), f"Sample file not found at: {SAMPLE_CSV}"

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
        check=False,
    )

    assert result.returncode == 0, f"Process crashed with error: {result.stderr}"
    assert "STUDY PLAN" in result.stdout
    assert "Assignment" in result.stdout
    assert "DS exam" in result.stdout
    assert "2.0h" in result.stdout


def test_e2e_cli_with_today_option() -> None:
    """Test CLI execution specifying --today option.

    Ensures tasks are ordered by urgency relative to the given reference date.
    """
    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(SAMPLE_CSV),
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
        check=False,
    )

    assert result.returncode == 0
    # Assignment (deadline 2026-10-27) is more urgent than DS exam (2026-10-30)
    pos_assignment = result.stdout.find("Assignment")
    pos_ds_exam = result.stdout.find("DS exam")
    assert pos_assignment != -1 and pos_ds_exam != -1
    assert pos_assignment < pos_ds_exam, (
        "Assignment should be prioritised before DS exam"
    )


def test_e2e_cli_verbose_logging() -> None:
    """Test CLI execution with verbose logging flag enabled."""
    cmd = [
        sys.executable,
        "-m",
        "shared.study_planner",
        str(SAMPLE_CSV),
        "--hours",
        "2",
        "--verbose",
    ]
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    combined = result.stdout + result.stderr
    assert "DEBUG" in combined or "INFO" in combined


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
        check=False,
    )

    assert result.returncode == 1
    assert "File not found" in (result.stdout + result.stderr) or "Error" in (
        result.stdout + result.stderr
    )


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
        check=False,
    )

    assert result.returncode == 1
    assert "empty" in (result.stdout + result.stderr).lower()


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
    assert "Total study time: 2.0h" in rendered
