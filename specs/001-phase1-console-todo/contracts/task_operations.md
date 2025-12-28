# Task Operations Contract

**Feature**: Phase I Console Todo
**Date**: 2025-12-28
**Module**: `src/application/task_service.py`

## Overview

This document defines the contract for the TaskService class, which provides all task management operations (CRUD + status toggle) for the Phase I console application.

## TaskService Interface

### Class: TaskService

**Responsibilities**:
- Manage in-memory task storage (dict)
- Generate unique sequential task IDs
- Validate task operations
- Return success/error indicators

**Dependencies**:
- `Task` entity from `src/domain/task.py`

**State**:
```python
tasks: dict[int, Task]  # In-memory storage, keyed by task ID
next_id: int            # Counter for ID generation, starts at 1
```

---

## Methods

### add_task

**Signature**:
```python
def add_task(self, description: str) -> Task | str
```

**Purpose**: Create a new task with auto-assigned ID and Incomplete status

**Parameters**:
- `description` (str): Task description provided by user

**Returns**:
- `Task`: On success, returns the created Task instance
- `str`: On validation failure, returns error message string

**Validation**:
1. Strip whitespace from description
2. Check description is not empty after stripping (FR-002)

**Behavior**:
1. Validate description (non-empty after strip)
2. If invalid: return error message "Task description cannot be empty"
3. Assign `id = self.next_id`
4. Increment `self.next_id` (never reuse IDs per SC-006)
5. Create Task with `is_complete=False` (FR-005)
6. Store in `self.tasks[id]`
7. Return created Task

**Spec References**: FR-002, FR-003, FR-005, SC-006

**Example**:
```python
service = TaskService()

# Success case
result = service.add_task("Buy groceries")
assert isinstance(result, Task)
assert result.id == 1
assert result.description == "Buy groceries"
assert result.is_complete == False

# Validation failure
result = service.add_task("   ")
assert isinstance(result, str)
assert result == "Task description cannot be empty"
```

---

### get_task

**Signature**:
```python
def get_task(self, task_id: int) -> Task | None
```

**Purpose**: Retrieve a task by ID (internal helper for other operations)

**Parameters**:
- `task_id` (int): Unique task identifier

**Returns**:
- `Task`: If task with given ID exists
- `None`: If task not found

**Behavior**:
1. Lookup `task_id` in `self.tasks`
2. Return Task if found, None otherwise

**Spec References**: FR-010 (ID validation)

**Example**:
```python
service = TaskService()
task = service.add_task("Test task")

# Found
result = service.get_task(task.id)
assert result == task

# Not found
result = service.get_task(999)
assert result is None
```

---

### list_tasks

**Signature**:
```python
def list_tasks(self) -> list[Task]
```

**Purpose**: Retrieve all tasks ordered by ID

**Parameters**: None

**Returns**:
- `list[Task]`: All tasks sorted by ID (ascending)
- Empty list if no tasks exist

**Behavior**:
1. Get all tasks from `self.tasks.values()`
2. Sort by Task ID (ascending)
3. Return sorted list

**Spec References**: FR-006 (display all tasks)

**Example**:
```python
service = TaskService()

# Empty list initially
assert service.list_tasks() == []

# After adding tasks
service.add_task("Task 1")
service.add_task("Task 2")
tasks = service.list_tasks()
assert len(tasks) == 2
assert tasks[0].id == 1
assert tasks[1].id == 2
```

---

### update_task

**Signature**:
```python
def update_task(self, task_id: int, new_description: str) -> bool | str
```

**Purpose**: Update a task's description

**Parameters**:
- `task_id` (int): ID of task to update
- `new_description` (str): New description text

**Returns**:
- `True`: On success
- `str`: On validation/not-found failure, returns error message

**Validation**:
1. Check task exists (FR-010)
2. Strip whitespace from new_description
3. Check new_description is not empty after stripping (FR-002)

**Behavior**:
1. Retrieve task using `get_task(task_id)`
2. If not found: return error message "Task ID not found"
3. Strip whitespace from `new_description`
4. If empty: return error message "Task description cannot be empty"
5. Update `task.description = new_description`
6. Return `True`

**Spec References**: FR-007, FR-010, FR-002

**Example**:
```python
service = TaskService()
task = service.add_task("Buy milk")

# Success case
result = service.update_task(task.id, "Buy organic milk")
assert result is True
assert service.get_task(task.id).description == "Buy organic milk"

# Task not found
result = service.update_task(999, "New description")
assert isinstance(result, str)
assert result == "Task ID not found"

# Empty description
result = service.update_task(task.id, "   ")
assert isinstance(result, str)
assert result == "Task description cannot be empty"
```

---

### delete_task

**Signature**:
```python
def delete_task(self, task_id: int) -> bool | str
```

**Purpose**: Delete a task by ID (ID not reused)

**Parameters**:
- `task_id` (int): ID of task to delete

**Returns**:
- `True`: On success
- `str`: On not-found failure, returns error message

**Validation**:
1. Check task exists (FR-010)

**Behavior**:
1. Check if `task_id` exists in `self.tasks`
2. If not found: return error message "Task ID not found"
3. Delete task: `del self.tasks[task_id]`
4. **Do NOT** decrement `next_id` (IDs never reused per SC-006)
5. Return `True`

**Spec References**: FR-008, FR-010, SC-006

**Example**:
```python
service = TaskService()
task1 = service.add_task("Task 1")
task2 = service.add_task("Task 2")

# Success case
result = service.delete_task(task1.id)
assert result is True
assert service.get_task(task1.id) is None
assert len(service.list_tasks()) == 1

# ID not reused
task3 = service.add_task("Task 3")
assert task3.id == 3  # Not 1, even though 1 was deleted

# Task not found
result = service.delete_task(999)
assert isinstance(result, str)
assert result == "Task ID not found"
```

---

### toggle_complete

**Signature**:
```python
def toggle_complete(self, task_id: int) -> bool | str
```

**Purpose**: Toggle task completion status (Complete ↔ Incomplete)

**Parameters**:
- `task_id` (int): ID of task to toggle

**Returns**:
- `True`: On success
- `str`: On not-found failure, returns error message

**Validation**:
1. Check task exists (FR-010)

**Behavior**:
1. Retrieve task using `get_task(task_id)`
2. If not found: return error message "Task ID not found"
3. Toggle `task.is_complete = not task.is_complete`
4. Return `True`

**Spec References**: FR-009, FR-010

**Note**: This unified method handles both "Mark Complete" and "Mark Incomplete" menu options by toggling the current state. The CLI layer is responsible for presenting separate menu choices.

**Example**:
```python
service = TaskService()
task = service.add_task("Test task")
assert task.is_complete == False

# Toggle to Complete
result = service.toggle_complete(task.id)
assert result is True
assert service.get_task(task.id).is_complete == True

# Toggle back to Incomplete
result = service.toggle_complete(task.id)
assert result is True
assert service.get_task(task.id).is_complete == False

# Task not found
result = service.toggle_complete(999)
assert isinstance(result, str)
assert result == "Task ID not found"
```

---

## Error Handling Strategy

**Philosophy**: Return error messages as strings rather than raising exceptions for business logic errors

**Rationale**:
- User input errors are expected and recoverable
- CLI can display error messages and re-prompt without crashes
- Meets SC-005 (100% invalid inputs handled gracefully)

**Error Types**:

| Error Condition | Return Value | Spec Reference |
|----------------|--------------|----------------|
| Empty description | `"Task description cannot be empty"` | FR-002, FR-011 |
| Task ID not found | `"Task ID not found"` | FR-010, FR-011 |
| No tasks available | *(Handled by CLI checking empty list)* | FR-011 |

**Success Types**:

| Operation | Success Return | Spec Reference |
|-----------|----------------|----------------|
| add_task | `Task` instance | FR-002 |
| get_task | `Task` instance or `None` | FR-010 |
| list_tasks | `list[Task]` (may be empty) | FR-006 |
| update_task | `True` | FR-007 |
| delete_task | `True` | FR-008 |
| toggle_complete | `True` | FR-009 |

---

## Thread Safety

**Phase I**: Not thread-safe (single-user, single-threaded CLI application)

**Rationale**: FR-013 specifies single-user usage. No concurrent access in Phase I.

**Future Phases**: Phase III+ will require thread-safe operations (locks or database transactions)

---

## Performance Guarantees

| Operation | Time Complexity | Spec Reference |
|-----------|----------------|----------------|
| add_task | O(1) | SC-001 (5 seconds) |
| get_task | O(1) | SC-002 (2 seconds) |
| list_tasks | O(n log n) | SC-002 (2 seconds) |
| update_task | O(1) | SC-003 |
| delete_task | O(1) | SC-003 |
| toggle_complete | O(1) | SC-003 |

**Note**: `list_tasks` is O(n log n) due to sorting, but n ≤ 100 per SC-008, so sub-second performance guaranteed

---

## Testing Strategy

### Unit Tests

**File**: `tests/unit/test_task_service.py`

**Coverage**:
- ✅ add_task: success, empty description, whitespace-only description
- ✅ get_task: found, not found
- ✅ list_tasks: empty, single task, multiple tasks (verify sorted by ID)
- ✅ update_task: success, task not found, empty description
- ✅ delete_task: success, task not found, ID not reused
- ✅ toggle_complete: success, toggle twice (round trip), task not found

**Target Coverage**: 100% (application layer business logic)

### Integration Tests

**File**: `tests/integration/test_cli_integration.py`

**Scenarios**:
- Add task → View list → Verify task displayed
- Add task → Update task → View list → Verify updated
- Add task → Delete task → View list → Verify removed
- Add task → Mark complete → View list → Verify status changed
- Add task → Mark complete → Mark incomplete → Verify status toggled

**Target Coverage**: 80%+ (end-to-end workflows)
