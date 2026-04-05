"""Unit tests for src/service.py."""
import pytest

from src.models import Priority, Task, TaskStatus
from src.repository import TaskNotFoundError, TaskRepository
from src.service import TaskService


class TestTaskService:
    def setup_method(self) -> None:
        self.repo = TaskRepository()
        self.service = TaskService(repo=self.repo)

    def test_create_task_returns_id(self) -> None:
        task_id = self.service.create_task("Write docs")
        assert task_id == 1

    def test_create_task_stores_task(self) -> None:
        task_id = self.service.create_task("Write docs")
        task = self.repo.get(task_id)
        assert task.title == "Write docs"

    def test_create_task_default_priority(self) -> None:
        task_id = self.service.create_task("Write docs")
        task = self.repo.get(task_id)
        assert task.priority == Priority.MEDIUM

    def test_create_task_custom_priority(self) -> None:
        task_id = self.service.create_task("Critical fix", priority=Priority.CRITICAL)
        task = self.repo.get(task_id)
        assert task.priority == Priority.CRITICAL

    def test_create_task_with_description(self) -> None:
        task_id = self.service.create_task("Deploy", description="Deploy to prod")
        task = self.repo.get(task_id)
        assert task.description == "Deploy to prod"

    def test_create_task_default_status_is_todo(self) -> None:
        task_id = self.service.create_task("New task")
        task = self.repo.get(task_id)
        assert task.status == TaskStatus.TODO

    def test_create_multiple_tasks_increments_ids(self) -> None:
        id1 = self.service.create_task("First")
        id2 = self.service.create_task("Second")
        assert id2 == id1 + 1

    def test_complete_task_marks_done(self) -> None:
        task_id = self.service.create_task("Finish report")
        self.service.complete_task(task_id)
        task = self.repo.get(task_id)
        assert task.status == TaskStatus.DONE

    def test_complete_task_sets_updated_at(self) -> None:
        task_id = self.service.create_task("Finish report")
        self.service.complete_task(task_id)
        task = self.repo.get(task_id)
        assert task.updated_at is not None

    def test_complete_task_raises_for_missing_id(self) -> None:
        with pytest.raises(TaskNotFoundError):
            self.service.complete_task(999)

    def test_cancel_task_marks_cancelled(self) -> None:
        task_id = self.service.create_task("Old feature")
        self.service.cancel_task(task_id)
        task = self.repo.get(task_id)
        assert task.status == TaskStatus.CANCELLED

    def test_cancel_task_sets_updated_at(self) -> None:
        task_id = self.service.create_task("Old feature")
        self.service.cancel_task(task_id)
        task = self.repo.get(task_id)
        assert task.updated_at is not None

    def test_cancel_task_raises_for_missing_id(self) -> None:
        with pytest.raises(TaskNotFoundError):
            self.service.cancel_task(999)

    def test_get_summary_empty(self) -> None:
        summary = self.service.get_summary()
        assert summary == {
            "total": 0,
            "todo": 0,
            "in_progress": 0,
            "done": 0,
            "cancelled": 0,
        }

    def test_get_summary_counts_all_statuses(self) -> None:
        id1 = self.service.create_task("Task 1")
        id2 = self.service.create_task("Task 2")
        id3 = self.service.create_task("Task 3")
        id4 = self.service.create_task("Task 4")

        self.service.complete_task(id2)
        self.service.cancel_task(id3)

        summary = self.service.get_summary()
        assert summary["total"] == 4
        assert summary["todo"] == 2
        assert summary["in_progress"] == 0
        assert summary["done"] == 1
        assert summary["cancelled"] == 1

    def test_service_uses_default_repo_when_none_provided(self) -> None:
        service = TaskService()
        task_id = service.create_task("Auto repo task")
        assert task_id == 1

    def test_service_uses_injected_repo(self) -> None:
        repo = TaskRepository()
        # Pre-populate the injected repo
        repo.add(Task(title="Existing task"))
        service = TaskService(repo=repo)
        summary = service.get_summary()
        assert summary["total"] == 1
