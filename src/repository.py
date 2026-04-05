"""In-memory task repository."""
import logging
from typing import Sequence

from .models import Task, TaskStatus, Priority

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""


class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> int:
        task_id = self._next_id
        self._tasks[task_id] = task
        self._next_id += 1
        logger.info("Task %d created: %s", task_id, task.title)
        return task_id

    def get(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def list_all(self) -> Sequence[Task]:
        return list(self._tasks.values())

    def list_by_status(self, status: TaskStatus) -> Sequence[Task]:
        return [t for t in self._tasks.values() if t.status == status]

    def list_by_priority(self, priority: Priority) -> Sequence[Task]:
        return [t for t in self._tasks.values() if t.priority == priority]

    def delete(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task {task_id} not found")
        del self._tasks[task_id]
        logger.info("Task %d deleted", task_id)
