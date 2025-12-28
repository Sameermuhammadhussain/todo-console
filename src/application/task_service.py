"""
TaskService - Application layer for task management operations.

Provides CRUD operations and status management for tasks following clean architecture.
"""
from typing import Union
from src.domain.task import Task


class TaskService:
    """
    Service class for managing todo tasks.

    Handles task operations (CRUD + toggle status) with in-memory storage.
    """

    def __init__(self):
        """Initialize TaskService with empty task storage."""
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, description: str) -> Union[Task, str]:
        """
        Create a new task with auto-assigned ID.

        Args:
            description: Task description provided by user

        Returns:
            Task instance on success, error message string on failure

        Spec Reference: FR-002, FR-003, FR-005
        """
        # Strip whitespace
        description = description.strip()

        # Validate non-empty
        if not description:
            return "Task description cannot be empty"

        # Create task with next available ID
        task_id = self.next_id
        self.next_id += 1

        try:
            task = Task(id=task_id, description=description, is_complete=False)
            self.tasks[task_id] = task
            return task
        except ValueError as e:
            return str(e)

    def get_task(self, task_id: int) -> Union[Task, None]:
        """
        Retrieve a task by ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task if found, None otherwise

        Spec Reference: FR-010
        """
        return self.tasks.get(task_id)

    def list_tasks(self) -> list[Task]:
        """
        Retrieve all tasks sorted by ID.

        Returns:
            List of all tasks ordered by ID (ascending), empty list if no tasks

        Spec Reference: FR-006
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def update_task(self, task_id: int, new_description: str) -> Union[bool, str]:
        """
        Update a task's description.

        Args:
            task_id: ID of task to update
            new_description: New description text

        Returns:
            True on success, error message string on failure

        Spec Reference: FR-007, FR-010, FR-002
        """
        # Check task exists
        task = self.get_task(task_id)
        if task is None:
            return "Task ID not found"

        # Strip and validate new description
        new_description = new_description.strip()
        if not new_description:
            return "Task description cannot be empty"

        # Update description
        task.description = new_description
        return True

    def delete_task(self, task_id: int) -> Union[bool, str]:
        """
        Delete a task by ID (ID not reused).

        Args:
            task_id: ID of task to delete

        Returns:
            True on success, error message string on failure

        Spec Reference: FR-008, FR-010, SC-006
        """
        # Check task exists
        if task_id not in self.tasks:
            return "Task ID not found"

        # Delete task (ID never reused per SC-006)
        del self.tasks[task_id]
        return True

    def toggle_complete(self, task_id: int) -> Union[bool, str]:
        """
        Toggle task completion status (Complete ↔ Incomplete).

        Args:
            task_id: ID of task to toggle

        Returns:
            True on success, error message string on failure

        Spec Reference: FR-009, FR-010
        """
        # Check task exists
        task = self.get_task(task_id)
        if task is None:
            return "Task ID not found"

        # Toggle status
        task.toggle_status()
        return True
