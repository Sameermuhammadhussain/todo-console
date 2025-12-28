"""
Integration tests for CLI application.

Tests follow TDD approach and verify end-to-end workflows.
"""
import pytest
from io import StringIO
import sys
from src.main import main
from src.application.task_service import TaskService
from src.infrastructure.cli import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete,
    handle_mark_incomplete
)


class TestAddTaskFlow:
    """Test add task integration flow."""

    def test_add_task_integration(self, monkeypatch, capsys):
        """Test adding a task through CLI."""
        service = TaskService()

        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "Buy groceries")

        handle_add_task(service)

        captured = capsys.readouterr()
        assert "Task added with ID 1" in captured.out

        # Verify task was added
        tasks = service.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Buy groceries"

    def test_add_task_with_empty_description(self, monkeypatch, capsys):
        """Test adding task with empty description shows error."""
        service = TaskService()

        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "")

        handle_add_task(service)

        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "cannot be empty" in captured.out.lower()


class TestViewTasksFlow:
    """Test view tasks integration flow."""

    def test_view_tasks_when_empty(self, capsys):
        """Test viewing tasks when no tasks exist."""
        service = TaskService()

        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out

    def test_view_tasks_with_multiple_tasks(self, capsys):
        """Test viewing multiple tasks displays all tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        handle_view_tasks(service)

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Task 3" in captured.out
        assert "Incomplete" in captured.out


class TestUpdateTaskFlow:
    """Test update task integration flow."""

    def test_update_task_integration(self, monkeypatch, capsys):
        """Test updating a task through CLI."""
        service = TaskService()
        service.add_task("Buy milk")

        # Mock user inputs: task ID, then new description
        inputs = iter(["1", "Buy organic milk"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        handle_update_task(service)

        captured = capsys.readouterr()
        assert "Task 1 updated successfully" in captured.out

        # Verify task was updated
        task = service.get_task(1)
        assert task.description == "Buy organic milk"

    def test_update_task_with_invalid_id(self, monkeypatch, capsys):
        """Test updating task with invalid ID shows error."""
        service = TaskService()
        service.add_task("Test task")

        # Mock user inputs
        inputs = iter(["999", "New description"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        handle_update_task(service)

        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "not found" in captured.out.lower()


class TestDeleteTaskFlow:
    """Test delete task integration flow."""

    def test_delete_task_integration(self, monkeypatch, capsys):
        """Test deleting a task through CLI."""
        service = TaskService()
        service.add_task("Task to delete")

        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "1")

        handle_delete_task(service)

        captured = capsys.readouterr()
        assert "Task 1 deleted successfully" in captured.out

        # Verify task was deleted
        task = service.get_task(1)
        assert task is None
        assert len(service.list_tasks()) == 0


class TestMarkCompleteFlow:
    """Test mark complete integration flow."""

    def test_mark_complete_integration(self, monkeypatch, capsys):
        """Test marking a task as complete through CLI."""
        service = TaskService()
        service.add_task("Test task")

        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "1")

        handle_mark_complete(service)

        captured = capsys.readouterr()
        assert "Task 1 marked as complete" in captured.out

        # Verify task status changed
        task = service.get_task(1)
        assert task.is_complete is True


class TestMarkIncompleteFlow:
    """Test mark incomplete integration flow."""

    def test_mark_incomplete_integration(self, monkeypatch, capsys):
        """Test marking a task as incomplete through CLI."""
        service = TaskService()
        task = service.add_task("Test task")
        task.mark_complete()

        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "1")

        handle_mark_incomplete(service)

        captured = capsys.readouterr()
        assert "Task 1 marked as incomplete" in captured.out

        # Verify task status changed
        task = service.get_task(1)
        assert task.is_complete is False
