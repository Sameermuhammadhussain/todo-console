"""
Unit tests for TaskService.

Tests follow TDD approach - written FIRST before implementation.
"""
import pytest
from src.application.task_service import TaskService
from src.domain.task import Task


class TestAddTask:
    """Test TaskService.add_task() method."""

    def test_add_task_success(self):
        """Test adding a valid task returns Task instance."""
        service = TaskService()

        result = service.add_task("Buy groceries")

        assert isinstance(result, Task)
        assert result.id == 1
        assert result.description == "Buy groceries"
        assert result.is_complete is False

    def test_add_task_assigns_sequential_ids(self):
        """Test that tasks get sequential IDs."""
        service = TaskService()

        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_description_returns_error(self):
        """Test adding task with empty description returns error string."""
        service = TaskService()

        result = service.add_task("")

        assert isinstance(result, str)
        assert "cannot be empty" in result.lower()

    def test_add_task_with_whitespace_only_description_returns_error(self):
        """Test adding task with whitespace-only description returns error."""
        service = TaskService()

        result = service.add_task("   ")

        assert isinstance(result, str)
        assert "cannot be empty" in result.lower()

    def test_add_task_strips_whitespace(self):
        """Test that task description whitespace is stripped."""
        service = TaskService()

        result = service.add_task("  Buy milk  ")

        assert isinstance(result, Task)
        assert result.description == "Buy milk"


class TestListTasks:
    """Test TaskService.list_tasks() method."""

    def test_list_tasks_empty(self):
        """Test listing tasks when no tasks exist returns empty list."""
        service = TaskService()

        tasks = service.list_tasks()

        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_list_tasks_with_multiple_tasks(self):
        """Test listing multiple tasks returns all tasks sorted by ID."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        tasks = service.list_tasks()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[0].description == "Task 1"
        assert tasks[1].id == 2
        assert tasks[1].description == "Task 2"
        assert tasks[2].id == 3
        assert tasks[2].description == "Task 3"

    def test_list_tasks_returns_sorted_by_id(self):
        """Test that list_tasks returns tasks sorted by ID in ascending order."""
        service = TaskService()
        service.add_task("First")
        service.add_task("Second")
        service.add_task("Third")

        tasks = service.list_tasks()

        assert [t.id for t in tasks] == [1, 2, 3]


class TestGetTask:
    """Test TaskService.get_task() helper method."""

    def test_get_task_found(self):
        """Test getting an existing task returns the task."""
        service = TaskService()
        added_task = service.add_task("Test task")

        result = service.get_task(added_task.id)

        assert result == added_task
        assert result.id == added_task.id
        assert result.description == "Test task"

    def test_get_task_not_found_returns_none(self):
        """Test getting a non-existent task returns None."""
        service = TaskService()

        result = service.get_task(999)

        assert result is None

    def test_get_task_after_adding_multiple_tasks(self):
        """Test getting specific task from multiple tasks."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        result = service.get_task(task2.id)

        assert result == task2
        assert result.id == 2
        assert result.description == "Task 2"


class TestToggleComplete:
    """Test TaskService.toggle_complete() method (User Story 2)."""

    def test_toggle_complete_success(self):
        """Test toggling task to complete returns True."""
        service = TaskService()
        task = service.add_task("Test task")

        result = service.toggle_complete(task.id)

        assert result is True
        assert service.get_task(task.id).is_complete is True

    def test_toggle_complete_with_invalid_id_returns_error(self):
        """Test toggling non-existent task returns error string."""
        service = TaskService()

        result = service.toggle_complete(999)

        assert isinstance(result, str)
        assert "not found" in result.lower()

    def test_toggle_complete_round_trip(self):
        """Test toggling twice returns to original state."""
        service = TaskService()
        task = service.add_task("Test task")

        service.toggle_complete(task.id)
        service.toggle_complete(task.id)

        assert service.get_task(task.id).is_complete is False


class TestUpdateTask:
    """Test TaskService.update_task() method (User Story 3)."""

    def test_update_task_success(self):
        """Test updating task description returns True."""
        service = TaskService()
        task = service.add_task("Buy milk")

        result = service.update_task(task.id, "Buy organic milk")

        assert result is True
        assert service.get_task(task.id).description == "Buy organic milk"

    def test_update_task_with_invalid_id_returns_error(self):
        """Test updating non-existent task returns error string."""
        service = TaskService()

        result = service.update_task(999, "New description")

        assert isinstance(result, str)
        assert "not found" in result.lower()

    def test_update_task_with_empty_description_returns_error(self):
        """Test updating task with empty description returns error."""
        service = TaskService()
        task = service.add_task("Test task")

        result = service.update_task(task.id, "   ")

        assert isinstance(result, str)
        assert "cannot be empty" in result.lower()


class TestDeleteTask:
    """Test TaskService.delete_task() method (User Story 4)."""

    def test_delete_task_success(self):
        """Test deleting task returns True and removes it."""
        service = TaskService()
        task = service.add_task("Task to delete")

        result = service.delete_task(task.id)

        assert result is True
        assert service.get_task(task.id) is None
        assert len(service.list_tasks()) == 0

    def test_delete_task_with_invalid_id_returns_error(self):
        """Test deleting non-existent task returns error string."""
        service = TaskService()

        result = service.delete_task(999)

        assert isinstance(result, str)
        assert "not found" in result.lower()

    def test_delete_task_id_not_reused(self):
        """Test that deleted task IDs are not reused."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        service.delete_task(task1.id)
        task3 = service.add_task("Task 3")

        assert task3.id == 3  # Not 1, even though 1 was deleted
        assert service.get_task(1) is None
