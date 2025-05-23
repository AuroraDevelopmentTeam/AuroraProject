#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run_ruff_check() -> int:
    """Run Ruff checks and return the exit code."""
    try:
        # Run Ruff linter
        subprocess.run(
            ["ruff", "check", "src", "tests", "--fix"],
            check=True,
        )

        # Run Ruff formatter
        subprocess.run(
            ["ruff", "format", "src", "tests"],
            check=True,
        )

        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return e.returncode


if __name__ == "__main__":
    # Ensure we're in the project root
    project_root = Path(__file__).parent.parent
    if not (project_root / "pyproject.toml").exists():
        print("Error: Must be run from the project root directory")
        sys.exit(1)

    sys.exit(run_ruff_check())
