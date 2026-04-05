"""CLI entry point for the task management system."""
import logging
import sys

from src.models import Priority
from src.service import TaskService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    service = TaskService()

    t1 = service.create_task("Write blog post", priority=Priority.HIGH)
    t2 = service.create_task("Review PR", description="Review the auth module PR")
    t3 = service.create_task("Fix flaky test", priority=Priority.CRITICAL)

    service.complete_task(t2)
    service.cancel_task(t3)

    summary = service.get_summary()
    print(f"Tasks: {summary}")


if __name__ == "__main__":
    main()
