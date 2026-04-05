"""Unit tests for src/models.py."""
import pytest

from src.models import Priority, Task, TaskStatus


class TestPriority:
    def test_values(self) -> None:
        assert Priority.LOW.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.HIGH.value == 3
        assert Priority.CRITICAL.value == 4

    def test_ordering(self) -> None:
        assert Priority.LOW.value < Priority.MEDIUM.value
        assert Priority.MEDIUM.value < Priority.HIGH.value
        assert Priority.HIGH.value < Priority.CRITICAL.value

    def test_members(self) -> None:
        members = list(Priority)
        assert len(members) == 4
        assert Priority.LOW in members
        assert Priority.MEDIUM in members
        assert Priority.HIGH in members
        assert Priority.CRITICAL in members


class TestTaskStatus:
    def test_values(self) -> None:
        assert TaskStatus.TODO.value == "todo"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.DONE.value == "done"
        assert TaskStatus.CANCELLED.value == "cancelled"

    def test_members(self) -> None:
        members = list(TaskStatus)
        assert len(members) == 4
        assert TaskStatus.TODO in members
        assert TaskStatus.IN_PROGRESS in members
        assert TaskStatus.DONE in members
        assert TaskStatus.CANCELLED in members


class TestTask:
    def test_default_values(self) -> None:
        task = Task(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert task.status == TaskStatus.TODO
        assert task.updated_at is None
        assert task.tags == []

    def test_custom_values(self) -> None:
        task = Task(
            title="Deploy app",
            description="Deploy to production",
            priority=Priority.CRITICAL,
            status=TaskStatus.IN_PROGRESS,
            tags=["ops", "deploy"],
        )
        assert task.title == "Deploy app"
        assert task.description == "Deploy to production"
        assert task.priority == Priority.CRITICAL
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.tags == ["ops", "deploy"]

    def test_created_at_set_on_creation(self) -> None:
        task = Task(title="Test")
        assert task.created_at is not None

    def test_tags_are_independent_per_instance(self) -> None:
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        task1.tags.append("important")
        assert task2.tags == []

    def test_mark_done(self) -> None:
        task = Task(title="Write tests")
        task.mark_done()
        assert task.status == TaskStatus.DONE
        assert task.updated_at is not None

    def test_mark_done_updates_updated_at(self) -> None:
        task = Task(title="Write tests")
        assert task.updated_at is None
        task.mark_done()
        assert task.updated_at is not None

    def test_mark_cancelled(self) -> None:
        task = Task(title="Write tests")
        task.mark_cancelled()
        assert task.status == TaskStatus.CANCELLED
        assert task.updated_at is not None

    def test_mark_cancelled_updates_updated_at(self) -> None:
        task = Task(title="Write tests")
        assert task.updated_at is None
        task.mark_cancelled()
        assert task.updated_at is not None

    def test_mark_done_then_cancelled(self) -> None:
        task = Task(title="Write tests")
        task.mark_done()
        first_updated = task.updated_at
        task.mark_cancelled()
        assert task.status == TaskStatus.CANCELLED
        assert task.updated_at is not None
        assert task.updated_at >= first_updated  # type: ignore[operator]
