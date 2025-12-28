"""
CLI infrastructure for Phase I Console Todo application.

Provides menu-driven interface for user interaction.
"""
from src.application.task_service import TaskService


def display_menu() -> None:
    """Display the main menu with all available options."""
    print("\n=== Todo List Manager ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Exit")
    print()


def handle_add_task(service: TaskService) -> None:
    """
    Handle adding a new task.

    Args:
        service: TaskService instance to use for adding task
    """
    description = input("Enter task description: ").strip()

    result = service.add_task(description)

    if isinstance(result, str):
        # Error message
        print(f"Error: {result}")
    else:
        # Success - result is Task instance
        print(f"Task added with ID {result.id}")


def handle_view_tasks(service: TaskService) -> None:
    """
    Handle viewing all tasks.

    Args:
        service: TaskService instance to use for retrieving tasks
    """
    tasks = service.list_tasks()

    if not tasks:
        print("No tasks found")
        return

    # Display tasks in table format
    print("\n{:<5} | {:<50} | {:<15}".format("ID", "Description", "Status"))
    print("-" * 75)

    for task in tasks:
        # Truncate long descriptions for display
        description = task.description
        if len(description) > 50:
            description = description[:47] + "..."

        print("{:<5} | {:<50} | {:<15}".format(
            task.id,
            description,
            task.get_status_display()
        ))


def handle_update_task(service: TaskService) -> None:
    """
    Handle updating a task's description.

    Args:
        service: TaskService instance to use for updating task
    """
    # Check if tasks exist
    if not service.list_tasks():
        print("No tasks available")
        return

    try:
        task_id_str = input("Enter task ID: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Please enter a valid number")
        return

    new_description = input("Enter new description: ").strip()

    result = service.update_task(task_id, new_description)

    if isinstance(result, str):
        # Error message
        print(f"Error: {result}")
    else:
        # Success
        print(f"Task {task_id} updated successfully")


def handle_delete_task(service: TaskService) -> None:
    """
    Handle deleting a task.

    Args:
        service: TaskService instance to use for deleting task
    """
    # Check if tasks exist
    if not service.list_tasks():
        print("No tasks available")
        return

    try:
        task_id_str = input("Enter task ID: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Please enter a valid number")
        return

    result = service.delete_task(task_id)

    if isinstance(result, str):
        # Error message
        print(f"Error: {result}")
    else:
        # Success
        print(f"Task {task_id} deleted successfully")


def handle_mark_complete(service: TaskService) -> None:
    """
    Handle marking a task as complete.

    Args:
        service: TaskService instance to use for toggling task
    """
    # Check if tasks exist
    if not service.list_tasks():
        print("No tasks available")
        return

    try:
        task_id_str = input("Enter task ID: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Please enter a valid number")
        return

    result = service.toggle_complete(task_id)

    if isinstance(result, str):
        # Error message
        print(f"Error: {result}")
    else:
        # Success
        print(f"Task {task_id} marked as complete")


def handle_mark_incomplete(service: TaskService) -> None:
    """
    Handle marking a task as incomplete.

    Args:
        service: TaskService instance to use for toggling task
    """
    # Check if tasks exist
    if not service.list_tasks():
        print("No tasks available")
        return

    try:
        task_id_str = input("Enter task ID: ")
        task_id = int(task_id_str)
    except ValueError:
        print("Please enter a valid number")
        return

    result = service.toggle_complete(task_id)

    if isinstance(result, str):
        # Error message
        print(f"Error: {result}")
    else:
        # Success
        print(f"Task {task_id} marked as incomplete")


def run_cli(service: TaskService) -> None:
    """
    Run the main CLI loop.

    Args:
        service: TaskService instance to use for all operations
    """
    while True:
        display_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            handle_add_task(service)
        elif choice == "2":
            handle_view_tasks(service)
        elif choice == "3":
            handle_update_task(service)
        elif choice == "4":
            handle_delete_task(service)
        elif choice == "5":
            handle_mark_complete(service)
        elif choice == "6":
            handle_mark_incomplete(service)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7")
