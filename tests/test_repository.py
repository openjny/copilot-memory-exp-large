"""Unit tests for src/repository.py."""
import pytest

from src.models import Priority, Task, TaskStatus
from src.repository import TaskNotFoundError, TaskRepository


class TestTaskRepository:
    def setup_method(self) -> None:
        self.repo = TaskRepository()

    def test_add_returns_id(self) -> None:
        task = Task(title="First task")
        task_id = self.repo.add(task)
        assert task_id == 1

    def test_add_increments_id(self) -> None:
        id1 = self.repo.add(Task(title="First"))
        id2 = self.repo.add(Task(title="Second"))
        id3 = self.repo.add(Task(title="Third"))
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3

    def test_get_returns_added_task(self) -> None:
        task = Task(title="My task", description="Do something")
        task_id = self.repo.add(task)
        retrieved = self.repo.get(task_id)
        assert retrieved is task

    def test_get_raises_for_missing_task(self) -> None:
        with pytest.raises(TaskNotFoundError):
            self.repo.get(999)

    def test_get_raises_with_message_containing_id(self) -> None:
        with pytest.raises(TaskNotFoundError, match="42"):
            self.repo.get(42)

    def test_list_all_empty_initially(self) -> None:
        assert list(self.repo.list_all()) == []

    def test_list_all_returns_all_tasks(self) -> None:
        t1 = Task(title="First")
        t2 = Task(title="Second")
        self.repo.add(t1)
        self.repo.add(t2)
        all_tasks = list(self.repo.list_all())
        assert len(all_tasks) == 2
        assert t1 in all_tasks
        assert t2 in all_tasks

    def test_list_by_status_returns_matching_tasks(self) -> None:
        t_todo = Task(title="To do", status=TaskStatus.TODO)
        t_done = Task(title="Done", status=TaskStatus.DONE)
        t_cancelled = Task(title="Cancelled", status=TaskStatus.CANCELLED)
        self.repo.add(t_todo)
        self.repo.add(t_done)
        self.repo.add(t_cancelled)

        todos = list(self.repo.list_by_status(TaskStatus.TODO))
        assert todos == [t_todo]

        done_tasks = list(self.repo.list_by_status(TaskStatus.DONE))
        assert done_tasks == [t_done]

    def test_list_by_status_returns_empty_when_none_match(self) -> None:
        self.repo.add(Task(title="A task", status=TaskStatus.TODO))
        assert list(self.repo.list_by_status(TaskStatus.IN_PROGRESS)) == []

    def test_list_by_priority_returns_matching_tasks(self) -> None:
        t_low = Task(title="Low", priority=Priority.LOW)
        t_high = Task(title="High", priority=Priority.HIGH)
        t_high2 = Task(title="High 2", priority=Priority.HIGH)
        self.repo.add(t_low)
        self.repo.add(t_high)
        self.repo.add(t_high2)

        high_tasks = list(self.repo.list_by_priority(Priority.HIGH))
        assert len(high_tasks) == 2
        assert t_high in high_tasks
        assert t_high2 in high_tasks

    def test_list_by_priority_returns_empty_when_none_match(self) -> None:
        self.repo.add(Task(title="A task", priority=Priority.MEDIUM))
        assert list(self.repo.list_by_priority(Priority.CRITICAL)) == []

    def test_delete_removes_task(self) -> None:
        task_id = self.repo.add(Task(title="To delete"))
        self.repo.delete(task_id)
        with pytest.raises(TaskNotFoundError):
            self.repo.get(task_id)

    def test_delete_reduces_list(self) -> None:
        id1 = self.repo.add(Task(title="First"))
        id2 = self.repo.add(Task(title="Second"))
        self.repo.delete(id1)
        remaining = list(self.repo.list_all())
        assert len(remaining) == 1
        assert remaining[0].title == "Second"

    def test_delete_raises_for_missing_task(self) -> None:
        with pytest.raises(TaskNotFoundError):
            self.repo.delete(999)

    def test_delete_raises_with_message_containing_id(self) -> None:
        with pytest.raises(TaskNotFoundError, match="7"):
            self.repo.delete(7)


class TestTaskNotFoundError:
    def test_is_exception(self) -> None:
        err = TaskNotFoundError("Task 1 not found")
        assert isinstance(err, Exception)

    def test_message(self) -> None:
        err = TaskNotFoundError("Task 5 not found")
        assert "5" in str(err)
