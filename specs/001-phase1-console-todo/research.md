# Research: Phase I Console Todo

**Feature**: Phase I Console Todo
**Date**: 2025-12-28
**Phase**: 0 (Research)

## Research Questions

This document captures research findings for technical decisions in Phase I implementation.

## 1. Python Best Practices for Console Applications

### Decision: Menu-Driven Loop Pattern

**Pattern Selected**:
```python
while True:
    display_menu()
    choice = input("Enter choice: ").strip()

    if choice == "1":
        handle_add_task()
    elif choice == "2":
        handle_view_tasks()
    elif choice == "3":
        handle_update_task()
    elif choice == "4":
        handle_delete_task()
    elif choice == "5":
        handle_mark_complete()
    elif choice == "6":
        handle_mark_incomplete()
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1-7")
```

**Rationale**:
- Standard Python idiom for menu-driven CLI applications
- Simple, readable, no external dependencies
- Meets FR-001 (menu-based interface) and FR-015 (return to menu)

**Alternatives Considered**:
- **argparse/click frameworks**: Rejected - adds external dependencies, overkill for menu-based interaction
- **Recursive function calls**: Rejected - risk of stack overflow in long sessions

### Input Validation Pattern

**Pattern Selected**:
```python
# String validation
description = input("Enter task description: ").strip()
if not description:
    print("Task description cannot be empty")
    return

# Integer validation
try:
    task_id = int(input("Enter task ID: "))
except ValueError:
    print("Please enter a valid number")
    return
```

**Rationale**:
- `.strip()` handles whitespace per FR-002
- try-except for integer parsing prevents crashes per SC-005
- Clear error messages per FR-011

### Error Handling Convention

**Strategy**:
- **Validation errors**: Display message, return to menu (no exceptions)
- **Integer parsing**: Catch `ValueError`, display error, re-prompt
- **Business logic errors**: Return error strings from service layer, display in CLI

**Rationale**:
- User errors are expected and recoverable (SC-005: 100% invalid inputs handled gracefully)
- No crashes on invalid input
- Consistent error message format

## 2. In-Memory Storage Selection

### Decision: Dict with Integer Keys

**Data Structure**:
```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

**Performance Analysis**:

| Operation | Dict | List |
|-----------|------|------|
| Lookup by ID | O(1) | O(n) |
| Insert | O(1) | O(1) |
| Delete | O(1) | O(n) |
| List all | O(n) | O(n) |

**Memory Footprint**:
- Task object: ~96 bytes (int id, str description ~50 chars, bool status, dict overhead)
- 100 tasks: ~10 KB
- Well within SC-008 requirement (100+ tasks without degradation)

**Rationale**:
- O(1) lookups critical for SC-002 (view within 2 seconds) and SC-001 (add within 5 seconds)
- Dict provides optimal performance for FR-010 (validate ID exists)
- No external dependencies (built-in Python)

**Alternatives Considered**:
- **List with linear search**: Rejected - O(n) lookups unacceptable for 100+ tasks
- **SQLite in-memory**: Rejected - violates FR-012 (no databases), adds dependency

### ID Generation Strategy

**Pattern Selected**:
```python
def add_task(self, description: str) -> Task | str:
    task_id = self.next_id
    self.next_id += 1  # Never reused
    task = Task(id=task_id, description=description, is_complete=False)
    self.tasks[task_id] = task
    return task
```

**Rationale**:
- Sequential IDs starting at 1 per FR-003
- IDs never reused even after delete per SC-006
- Simple integer counter, no UUID complexity needed for Phase I

**Alternatives Considered**:
- **UUID**: Rejected - overly complex for Phase I, harder to type for users
- **Reuse deleted IDs**: Rejected - violates SC-006 (IDs remain unique throughout session)

## 3. Testing Strategy

### Unit Testing with pytest

**Pattern Selected**:
```python
# tests/unit/test_task_service.py
import pytest
from src.domain.task import Task
from src.application.task_service import TaskService

def test_add_task_success():
    service = TaskService()
    result = service.add_task("Buy milk")

    assert isinstance(result, Task)
    assert result.id == 1
    assert result.description == "Buy milk"
    assert result.is_complete == False

def test_add_task_empty_description():
    service = TaskService()
    result = service.add_task("")

    assert isinstance(result, str)
    assert "cannot be empty" in result
```

**Rationale**:
- pytest mandated by constitution
- Test both success and error paths per SC-004 and SC-005
- Mock storage dict for isolation (no real persistence)

### Integration Testing

**Pattern Selected**:
```python
# tests/integration/test_cli_integration.py
import pytest
from io import StringIO
import sys

def test_add_and_view_task(monkeypatch, capsys):
    # Mock user inputs
    inputs = iter(["1", "Buy groceries", "2", "7"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Run CLI
    from src.main import main
    main()

    # Capture output
    captured = capsys.readouterr()
    assert "Task added with ID 1" in captured.out
    assert "Buy groceries" in captured.out
    assert "Incomplete" in captured.out
```

**Rationale**:
- `monkeypatch` mocks `input()` for automated testing
- `capsys` captures `print()` output for verification
- Tests full user flows per acceptance scenarios in spec.md

### Coverage Target

**Requirement**: 80% minimum per constitution Principle V

**Strategy**:
- 100% coverage for domain layer (Task entity)
- 100% coverage for application layer (TaskService)
- 80%+ coverage for infrastructure layer (CLI - focus on logic, not display formatting)

**Tool**: pytest-cov
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Rationale**:
- High coverage for business logic ensures reliability
- Slightly lower for presentation layer acceptable (formatting code less critical)

## 4. Clean Architecture for Phase I

### Decision: Three-Layer Architecture

**Layers**:
1. **Domain**: Task entity (business rules, validation)
2. **Application**: TaskService (use cases, orchestration)
3. **Infrastructure**: CLI (user interface, I/O)

**Dependency Direction**:
```
Infrastructure (CLI) → Application (TaskService) → Domain (Task)
```

**Rationale**:
- Constitution Principle V mandates clean architecture
- Prepares for Phase III migration to FastAPI (replace CLI with HTTP handlers)
- Domain logic isolated from framework and UI concerns

**Trade-offs**:
- **Pro**: Easy to evolve in future phases, testable, maintainable
- **Con**: More files and structure than single-file script
- **Justification**: Constitution requirement, future-proof design

**Alternatives Considered**:
- **Single-file script**: Rejected - violates constitution Principle V (clean architecture)
- **MVC pattern**: Rejected - overkill for Phase I, three layers sufficient

## Summary

All research questions resolved:
- ✅ Console application pattern: Menu-driven loop
- ✅ Data structure: Dict with integer keys
- ✅ ID generation: Sequential counter starting at 1
- ✅ Testing strategy: pytest with monkeypatch for CLI
- ✅ Architecture: Clean architecture (domain/application/infrastructure)

**No NEEDS CLARIFICATION remaining** - ready for Phase 1 design.
