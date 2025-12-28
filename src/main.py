"""
Main entry point for Phase I Console Todo application.

Initializes the application and launches the CLI.
"""
from src.application.task_service import TaskService
from src.infrastructure.cli import run_cli


def main() -> None:
    """Initialize TaskService and launch CLI."""
    service = TaskService()
    run_cli(service)


if __name__ == "__main__":
    main()
