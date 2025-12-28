"""
Unit tests for Task entity.

Tests follow TDD approach - written FIRST before implementation.
"""
import pytest
from src.domain.task import Task


class TestTaskCreation:
    """Test Task entity creation."""

    def test_task_creation_success(self):
        """Test creating a valid task."""
        task = Task(id=1, description="Buy groceries", is_complete=False)

        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.is_complete is False

    def test_task_creation_with_default_status(self):
        """Test task defaults to incomplete status."""
        task = Task(id=2, description="Finish report")

        assert task.id == 2
        assert task.description == "Finish report"
        assert task.is_complete is False

    def test_task_creation_with_complete_status(self):
        """Test creating a completed task."""
        task = Task(id=3, description="Review code", is_complete=True)

        assert task.id == 3
        assert task.description == "Review code"
        assert task.is_complete is True


class TestTaskValidation:
    """Test Task entity validation rules."""

    def test_task_with_empty_description_raises_error(self):
        """Test that empty description raises ValueError."""
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            Task(id=1, description="", is_complete=False)

    def test_task_with_whitespace_only_description_raises_error(self):
        """Test that whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            Task(id=1, description="   ", is_complete=False)

    def test_task_with_invalid_id_raises_error(self):
        """Test that ID less than 1 raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=0, description="Invalid task", is_complete=False)

    def test_task_with_negative_id_raises_error(self):
        """Test that negative ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(id=-1, description="Invalid task", is_complete=False)

    def test_task_strips_whitespace_from_description(self):
        """Test that description whitespace is stripped."""
        task = Task(id=1, description="  Buy milk  ", is_complete=False)

        assert task.description == "Buy milk"


class TestTaskHelperMethods:
    """Test Task entity helper methods."""

    def test_mark_complete(self):
        """Test marking task as complete."""
        task = Task(id=1, description="Test task", is_complete=False)

        task.mark_complete()

        assert task.is_complete is True

    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task(id=1, description="Test task", is_complete=True)

        task.mark_incomplete()

        assert task.is_complete is False

    def test_toggle_status_from_incomplete_to_complete(self):
        """Test toggling status from incomplete to complete."""
        task = Task(id=1, description="Test task", is_complete=False)

        task.toggle_status()

        assert task.is_complete is True

    def test_toggle_status_from_complete_to_incomplete(self):
        """Test toggling status from complete to incomplete."""
        task = Task(id=1, description="Test task", is_complete=True)

        task.toggle_status()

        assert task.is_complete is False

    def test_toggle_status_round_trip(self):
        """Test toggling status twice returns to original state."""
        task = Task(id=1, description="Test task", is_complete=False)

        task.toggle_status()
        task.toggle_status()

        assert task.is_complete is False

    def test_get_status_display_incomplete(self):
        """Test status display for incomplete task."""
        task = Task(id=1, description="Test task", is_complete=False)

        assert task.get_status_display() == "Incomplete"

    def test_get_status_display_complete(self):
        """Test status display for complete task."""
        task = Task(id=1, description="Test task", is_complete=True)

        assert task.get_status_display() == "Complete"
