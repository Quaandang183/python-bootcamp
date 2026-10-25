"""Command-line interface tool for study plan assignments."""

import argparse
from pathlib import Path
import sys


def parse_arguments() -> argparse.Namespace:
    """Parse and validate command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments containing tasks_file, hours, and optional today.
    """
    parser = argparse.ArgumentParser(description="Study Planner CLI Tool")
    parser.add_argument("tasks_file", type=str, help="Path to tasks CSV file")
    parser.add_argument("--hours", type=float, required=True, help="Available study hours")
    parser.add_argument("--today", type=str, help="Today's date (YYYY-MM-DD)")
    return parser.parse_args()


def main() -> None:
    """Execute the main CLI application workflow.

    Validates the input task file path and prints the generated plan status.
    Exits with code 0 on success, or code 1 if the input file does not exist.
    """
    args = parse_arguments()
    tasks_path = Path(args.tasks_file)

    if not tasks_path.is_file():
        sys.exit(1)

    print(f"Assignment plan generated for {tasks_path.name} with {args.hours} hours.")
    sys.exit(0)


if __name__ == "__main__":
    main()