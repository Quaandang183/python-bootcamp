"""Integration test runner bridging tests/ to shared/study_planner/test_e2e.py."""

from shared.study_planner.test_e2e import (
    test_e2e_cli_empty_file,
    test_e2e_cli_missing_file,
    test_e2e_cli_missing_required_hours,
    test_e2e_cli_valid_sample,
    test_e2e_cli_verbose_logging,
    test_e2e_cli_with_today_option,
    test_pipeline_programmatic_flow,
)

__all__ = [
    "test_e2e_cli_empty_file",
    "test_e2e_cli_missing_file",
    "test_e2e_cli_missing_required_hours",
    "test_e2e_cli_valid_sample",
    "test_e2e_cli_verbose_logging",
    "test_e2e_cli_with_today_option",
    "test_pipeline_programmatic_flow",
]
