"""Main entry point for shared.study_planner CLI."""

import argparse
import logging
import sys
from datetime import date, datetime
from pathlib import Path

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render
from shared.study_planner.validate import InfeasiblePlan, check_feasible

logger = logging.getLogger("study_planner")


def setup_logging(verbose: bool) -> None:
    """Configure logging format and level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the study planner."""
    parser = argparse.ArgumentParser(
        description="Study Planner CLI - Automated study schedule generator"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to tasks CSV file",
    )
    parser.add_argument(
        "--hours",
        type=float,
        required=True,
        help="Available study hours (e.g. --hours 2)",
    )
    parser.add_argument(
        "--today",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=date.today(),
        help="Reference date formatted as YYYY-MM-DD (default: today)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose / DEBUG logging",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Execute the study planner pipeline and print the result."""
    args = parse_args(argv)
    setup_logging(args.verbose)

    logger.debug("Starting Study Planner...")
    logger.debug(
        "Parameters: file=%s, hours=%s, today=%s",
        args.file,
        args.hours,
        args.today,
    )

    try:
        # 1. Check file existence
        if not args.file.is_file():
            raise FileNotFoundError(f"File not found: {args.file}")

        # 2. Parse CSV
        logger.info("Reading tasks from %s...", args.file)
        tasks = parse_csv(str(args.file))
        if not tasks:
            raise ValueError(f"Task list is empty: {args.file}")

        # 3. Check feasibility (optional / warning if time exceeded)
        logger.info("Checking plan feasibility...")
        try:
            check_feasible(tasks, available_h=args.hours)
        except InfeasiblePlan as inf_err:
            logger.warning(
                "Warning: Total tasks effort exceeds available hours: %s", inf_err
            )

        # 4. Prioritise tasks
        logger.info("Prioritising tasks based on urgency and importance...")
        ordered = prioritise(tasks, today=args.today)

        # 5. Allocate time blocks
        logger.info("Allocating time blocks within %.1f hours...", args.hours)
        blocks = allocate(ordered, hours=args.hours)

        # 6. Render schedule
        logger.info("Rendering study plan output:")
        output_text = render(blocks)
        print(output_text)
        return 0

    except FileNotFoundError as e:
        logger.error("File error: %s", e)
        sys.stderr.write(f"Error: {e}\n")
        return 1
    except ValueError as e:
        logger.error("Data error: %s", e)
        sys.stderr.write(f"Error: {e}\n")
        return 1
    except InfeasiblePlan as e:
        logger.error("Feasibility error: %s", e)
        sys.stderr.write(f"Error: {e}\n")
        return 1
    except (OSError, RuntimeError) as e:
        logger.error("System error: %s", e)
        sys.stderr.write(f"System error: {e}\n")
        return 1


def main() -> None:
    """Entry point for command-line execution."""
    sys.exit(run())


if __name__ == "__main__":
    main()
