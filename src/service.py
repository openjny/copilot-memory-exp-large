"""Business logic for task management."""
import logging
from datetime import datetime, timezone

from .models import Task, Priority, TaskStatus
from .repository import TaskRepository

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repo: TaskRepository | None = None) -> None:
        self._repo = repo or TaskRepository()

    def create_task(
        self, title: str, description: str = "", priority: Priority = Priority.MEDIUM
    ) -> int:
        task = Task(title=title, description=description, priority=priority)
        return self._repo.add(task)

    def complete_task(self, task_id: int) -> None:
        task = self._repo.get(task_id)
        task.mark_done()
        logger.info("Task %d completed", task_id)

    def cancel_task(self, task_id: int) -> None:
        task = self._repo.get(task_id)
        task.mark_cancelled()
        logger.info("Task %d cancelled", task_id)

    def get_summary(self) -> dict[str, int]:
        all_tasks = self._repo.list_all()
        return {
            "total": len(all_tasks),
            "todo": len([t for t in all_tasks if t.status == TaskStatus.TODO]),
            "in_progress": len([t for t in all_tasks if t.status == TaskStatus.IN_PROGRESS]),
            "done": len([t for t in all_tasks if t.status == TaskStatus.DONE]),
            "cancelled": len([t for t in all_tasks if t.status == TaskStatus.CANCELLED]),
        }
