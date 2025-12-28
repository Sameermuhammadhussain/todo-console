"""
Task entity for Phase I Console Todo application.

This module defines the core Task entity following clean architecture principles.
The Task entity is the domain model representing a single todo item.
"""
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique sequential integer identifier (auto-assigned by service)
        description: Text describing what needs to be done (min 1 char after strip)
        is_complete: Completion status (False = Incomplete, True = Complete)
    """

    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """
        Validate task attributes after initialization.

        Raises:
            ValueError: If id is not a positive integer or description is empty.
        """
        # Validate ID
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        # Validate description type
        if not isinstance(self.description, str):
            raise ValueError("Task description must be a string")

        # Strip whitespace and validate non-empty
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("Task description cannot be empty")

        # Validate status type
        if not isinstance(self.is_complete, bool):
            raise ValueError("Task status must be a boolean")

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_complete = False

    def toggle_status(self) -> None:
        """Toggle task completion status between Complete and Incomplete."""
        self.is_complete = not self.is_complete

    def get_status_display(self) -> str:
        """
        Get human-readable status string.

        Returns:
            "Complete" if task is complete, "Incomplete" otherwise.
        """
        return "Complete" if self.is_complete else "Incomplete"
