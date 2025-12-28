"""
Performance tests for Phase I Console Todo.

Verifies success criteria SC-001, SC-002, and SC-008.
"""
import time
from src.application.task_service import TaskService


class TestPerformance:
    """Test performance requirements from spec.md."""

    def test_add_100_tasks_performance(self):
        """Test adding 100 tasks completes within reasonable time (SC-008)."""
        service = TaskService()

        start_time = time.time()

        for i in range(100):
            result = service.add_task(f"Task {i + 1}")
            assert not isinstance(result, str), f"Failed to add task {i + 1}"

        elapsed = time.time() - start_time

        # SC-001: Add task within 5 seconds
        # For 100 tasks, should be well under 5 seconds total
        assert elapsed < 5.0, f"Adding 100 tasks took {elapsed:.2f}s (should be < 5s)"
        print(f"\n✓ Added 100 tasks in {elapsed:.4f}s (average {elapsed/100*1000:.2f}ms per task)")

    def test_view_100_tasks_performance(self):
        """Test viewing 100 tasks completes within reasonable time (SC-002)."""
        service = TaskService()

        # Add 100 tasks
        for i in range(100):
            service.add_task(f"Task {i + 1}")

        start_time = time.time()
        tasks = service.list_tasks()
        elapsed = time.time() - start_time

        assert len(tasks) == 100
        # SC-002: View tasks within 2 seconds
        assert elapsed < 2.0, f"Viewing 100 tasks took {elapsed:.2f}s (should be < 2s)"
        print(f"✓ Viewed 100 tasks in {elapsed:.4f}s")

    def test_operations_with_100_tasks(self):
        """Test all operations work correctly with 100 tasks (SC-008)."""
        service = TaskService()

        # Add 100 tasks
        for i in range(100):
            task = service.add_task(f"Task {i + 1}")
            assert isinstance(task.id, int)

        # Verify all tasks present
        tasks = service.list_tasks()
        assert len(tasks) == 100

        # Test get_task with large ID
        task_100 = service.get_task(100)
        assert task_100 is not None
        assert task_100.id == 100

        # Test update_task
        result = service.update_task(50, "Updated task 50")
        assert result is True
        assert service.get_task(50).description == "Updated task 50"

        # Test toggle_complete
        result = service.toggle_complete(75)
        assert result is True
        assert service.get_task(75).is_complete is True

        # Test delete_task
        result = service.delete_task(25)
        assert result is True
        assert service.get_task(25) is None
        assert len(service.list_tasks()) == 99

        print("✓ All operations work correctly with 100+ tasks")

    def test_sequential_id_generation_at_scale(self):
        """Test IDs remain sequential and unique with many tasks (SC-006)."""
        service = TaskService()

        # Add 50 tasks
        for i in range(50):
            service.add_task(f"Task {i + 1}")

        # Delete some tasks
        service.delete_task(10)
        service.delete_task(20)
        service.delete_task(30)

        # Add more tasks - IDs should not be reused
        task_51 = service.add_task("Task 51")
        task_52 = service.add_task("Task 52")

        assert task_51.id == 51  # Not 10, 20, or 30
        assert task_52.id == 52

        # Verify deleted IDs are not in the list
        tasks = service.list_tasks()
        task_ids = [t.id for t in tasks]
        assert 10 not in task_ids
        assert 20 not in task_ids
        assert 30 not in task_ids
        assert 51 in task_ids
        assert 52 in task_ids

        print("✓ IDs remain unique and sequential (never reused)")
