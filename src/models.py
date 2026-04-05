"""Data models for the task management system."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Task:
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    tags: list[str] = field(default_factory=list)

    def mark_done(self) -> None:
        self.status = TaskStatus.DONE
        self.updated_at = datetime.now(timezone.utc)

    def mark_cancelled(self) -> None:
        self.status = TaskStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
