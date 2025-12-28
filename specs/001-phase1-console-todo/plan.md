# Implementation Plan: Phase I Console Todo

**Branch**: `001-phase1-console-todo` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-console-todo/spec.md`

## Summary

Implement an in-memory Python console application for basic task management (CRUD operations). Application provides a menu-based CLI for adding, viewing, updating, deleting, and toggling completion status of tasks. All data stored in memory with no persistence. Single-user, session-scoped application.

**Technical Approach**: Clean architecture with clear separation between domain (Task entity), application (task operations), and infrastructure (CLI presentation). Use Python dict for in-memory storage keyed by task ID, with a counter for ID generation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (standard library only for Phase I)
**Storage**: In-memory (Python dict)
**Testing**: pytest
**Target Platform**: Cross-platform (Windows, Linux, macOS)
**Project Type**: Single project (console application)
**Performance Goals**: Sub-second response for all operations with up to 100 tasks
**Constraints**: No external dependencies, no persistence, in-memory only, single user
**Scale/Scope**: 100+ tasks per session, single Python module initially

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Principles Compliance

**✅ I. Spec-Driven Development (Mandatory)**
- Plan derived strictly from approved spec.md
- No new features introduced beyond specification
- Architecture decisions documented in this plan

**✅ II. Agent Behavior Rules**
- Following specification exactly as written
- No autonomous feature invention
- Plan focuses on HOW to implement approved WHAT

**✅ III. Phase Governance**
- Strictly Phase I scope: console CRUD only
- No Phase II+ features (categories, deadlines, recurring tasks)
- No database, no web, no multi-user concepts
- In-memory storage enforced

**✅ IV. Technology Constraints**
- Python 3.11+ as mandated
- Standard library only (no frameworks for Phase I)
- pytest for testing (Phase I appropriate)
- No prohibited technologies introduced

**✅ V. Quality & Architecture Principles**
- Clean Architecture: Domain, Application, Infrastructure layers
- Separation of Concerns: Task entity, operations, CLI separated
- Single Responsibility Principle enforced
- Testing discipline: Unit tests for domain/application logic

### Architecture Decisions for Phase I

**Decision 1: Layered Architecture (Clean Architecture Lite)**
- **Domain Layer**: Task entity with business rules
- **Application Layer**: Task operations (add, update, delete, mark complete)
- **Infrastructure Layer**: CLI menu, input/output handling
- **Rationale**: Prepares codebase for Phase III migration to web/API by isolating business logic from presentation
- **Trade-off**: Slightly more complex than single-file approach, but maintains constitution principle V

**Decision 2: In-Memory Storage Strategy**
- **Choice**: Python dict keyed by task ID (integer)
- **Rationale**: O(1) lookups, simple, no external dependencies
- **Alternative Rejected**: List with linear search - O(n) lookups unacceptable for 100+ tasks
- **Phase I Constraint**: No databases, no files per FR-012

**Decision 3: ID Generation**
- **Choice**: Simple integer counter starting at 1, never reused
- **Rationale**: Sequential IDs per FR-003, remains unique even after deletions per SC-006
- **Alternative Rejected**: UUID - overly complex for Phase I scope

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-console-todo/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Python best practices, testing patterns)
├── data-model.md        # Phase 1 output (Task entity definition)
├── quickstart.md        # Phase 1 output (How to run and test)
├── contracts/           # Phase 1 output (Module interfaces)
│   └── task_operations.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── domain/
│   └── task.py          # Task entity: dataclass with id, description, status
├── application/
│   └── task_service.py  # TaskService: add, update, delete, get, list, toggle operations
├── infrastructure/
│   └── cli.py           # CLI: menu loop, input handling, output formatting
└── main.py              # Entry point: initialize service, launch CLI

tests/
├── unit/
│   ├── test_task.py            # Task entity unit tests
│   └── test_task_service.py    # TaskService unit tests
└── integration/
    └── test_cli_integration.py # End-to-end CLI tests
```

**Structure Decision**: Single project structure (Option 1) selected. Phase I is a standalone console application with no frontend/backend split. Clean architecture enforced through `domain/`, `application/`, and `infrastructure/` separation.

## Complexity Tracking

**No violations**: All constitution principles followed. Clean architecture is mandated by Principle V, justified by future-phase scalability needs.

---

## Phase 0: Research

### Research Questions

1. **Python Best Practices for Console Applications**
   - Input validation patterns
   - Error handling conventions
   - Menu-driven CLI patterns

2. **In-Memory Data Structure Selection**
   - Dict vs List performance characteristics
   - ID generation strategies
   - Memory footprint for 100+ tasks

3. **Testing Strategy for Console Applications**
   - Pytest patterns for CLI testing
   - Mocking stdin/stdout
   - Integration test approaches

### Research Findings

#### 1. Python Console Application Patterns

**Decision**: Menu-driven loop with numbered choices

**Pattern**:
```python
while True:
    display_menu()
    choice = input("Enter choice: ")
    if choice == "1":
        handle_add_task()
    elif choice == "2":
        handle_view_tasks()
    # ... etc
    elif choice == "7":
        break  # Exit
```

**Input Validation**:
- Use `input().strip()` to remove whitespace
- Validate non-empty strings before processing
- Catch `ValueError` for integer parsing
- Display error and re-prompt on invalid input

**Error Handling Convention**:
- Validation errors: Display message, return to menu (FR-011, FR-015)
- Use try-except for integer parsing
- No crashes on invalid input (SC-005)

**Rationale**: Standard Python idiom, simple, meets all FR requirements

**Alternative Rejected**: argparse/click CLI frameworks - overkill for Phase I, adds dependencies

#### 2. In-Memory Storage

**Decision**: Dict with integer keys

**Implementation**:
```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

**Performance**:
- Dict lookup: O(1) - meets SC-002 (2 second view requirement)
- Dict insert: O(1) - meets SC-001 (5 second add requirement)
- Memory: ~100 bytes per task × 100 tasks = ~10KB (well within SC-008)

**ID Generation**:
- Increment `next_id` counter on each add
- Never reuse IDs even after delete (meets SC-006)
- Start at 1 (meets FR-003)

**Rationale**: Optimal performance, simple, no external dependencies

**Alternative Rejected**: List - requires O(n) search for ID lookups, unacceptable for 100+ tasks

#### 3. Testing Strategy

**Unit Testing with pytest**:
- Test Task entity: validation, state transitions
- Test TaskService: CRUD operations, error cases
- Mock storage dict for isolation

**Integration Testing**:
- Use `monkeypatch` to mock `input()` and capture `print()` output
- Test full user flows: add → view → update → delete
- Verify error messages for invalid inputs

**Coverage Target**: 80% minimum per constitution Principle V

**Rationale**: pytest is mandated by constitution, patterns are industry-standard

**Alternative Rejected**: unittest - pytest is more concise and mandated

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Task Entity**:
- **id**: int (unique, sequential, auto-assigned)
- **description**: str (min 1 char after strip, no max)
- **is_complete**: bool (default False)

**Validation Rules**:
- Description must not be empty after stripping whitespace (FR-002)
- ID must be positive integer (enforced by counter starting at 1)
- Status is boolean (True = Complete, False = Incomplete)

### Application Layer Contracts

See [contracts/task_operations.md](./contracts/task_operations.md) for complete interface.

**TaskService Operations**:

```python
class TaskService:
    def add_task(description: str) -> Task | str
        # Returns: Task on success, error message string on validation failure
        # Validates: non-empty description (FR-002)
        # Assigns: next available ID (FR-003), status=Incomplete (FR-005)

    def get_task(task_id: int) -> Task | None
        # Returns: Task if found, None if not found
        # Used by: update, delete, toggle operations for validation (FR-010)

    def list_tasks() -> list[Task]
        # Returns: All tasks ordered by ID
        # Empty list if no tasks (supports "No tasks found" message)

    def update_task(task_id: int, new_description: str) -> bool | str
        # Returns: True on success, error message string on failure
        # Validates: task exists (FR-010), description non-empty (FR-002)

    def delete_task(task_id: int) -> bool | str
        # Returns: True on success, error message string on failure
        # Validates: task exists (FR-010)
        # Note: ID not reused after delete (SC-006)

    def toggle_complete(task_id: int) -> bool | str
        # Returns: True on success, error message string on failure
        # Validates: task exists (FR-010)
        # Toggles: is_complete between True/False (FR-009)
```

**Error Handling Strategy**:
- Operations return success (Task/bool) or error (str message)
- Caller (CLI) displays error messages and re-prompts
- No exceptions for business logic errors (empty task list, invalid ID)
- Exceptions only for programmer errors (None checks)

### Infrastructure Layer (CLI)

**Menu Options** (FR-001):
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

**Input/Output Flow**:

**Add Task**:
1. Prompt: "Enter task description: "
2. Read input, strip whitespace
3. Call `service.add_task(description)`
4. If success: Display "Task added with ID {id}"
5. If error: Display error message
6. Return to menu (FR-015)

**View Tasks**:
1. Call `service.list_tasks()`
2. If empty: Display "No tasks found"
3. Else: Display table format:
   ```
   ID  | Description          | Status
   ----|---------------------|----------
   1   | Buy groceries       | Incomplete
   2   | Finish report       | Complete
   ```
4. Return to menu (FR-015)

**Update Task**:
1. Check if tasks exist, else display "No tasks available"
2. Prompt: "Enter task ID: "
3. Parse integer, handle ValueError
4. Prompt: "Enter new description: "
5. Call `service.update_task(id, new_description)`
6. Display success or error message
7. Return to menu (FR-015)

**Delete Task**:
1. Check if tasks exist, else display "No tasks available"
2. Prompt: "Enter task ID: "
3. Parse integer, handle ValueError
4. Call `service.delete_task(id)`
5. Display success or error message
6. Return to menu (FR-015)

**Mark Complete/Incomplete**:
1. Check if tasks exist, else display "No tasks available"
2. Prompt: "Enter task ID: "
3. Parse integer, handle ValueError
4. Call `service.toggle_complete(id)` (unified operation)
5. Display success or error message
6. Return to menu (FR-015)

**Exit**:
1. Display "Goodbye!"
2. Break menu loop
3. Application terminates, memory cleared (FR-014)

**Error Messages** (FR-011):
- Empty description: "Task description cannot be empty"
- Invalid ID: "Task ID not found"
- No tasks available: "No tasks available"
- Invalid menu choice: "Invalid choice. Please enter 1-7"
- Non-numeric ID: "Please enter a valid number"

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup and usage instructions.

**Run Application**:
```bash
python src/main.py
```

**Run Tests**:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Expected Coverage**: 80%+ per constitution requirement

---

## Post-Design Constitution Re-Check

**✅ All gates passed**:
- Clean architecture maintained (domain/application/infrastructure)
- No Phase II+ features introduced
- Python 3.11+ with pytest only
- In-memory storage enforced
- Single responsibility principle per module
- 80% test coverage target set

**Architecture Decisions Requiring Documentation**:

📋 **Architectural decision detected**: Clean Architecture layering for Phase I console app
- **Context**: Phase I is simple console CRUD, could be single-file
- **Decision**: Three-layer architecture (domain, application, infrastructure)
- **Rationale**: Constitution Principle V mandates clean architecture; prepares for Phase III web migration
- **Trade-off**: More files/complexity now, but easier evolution to FastAPI in Phase III

Document this decision? Run `/sp.adr clean-architecture-phase1`

---

## Next Steps

1. **User Approval**: Review and approve this plan
2. **Generate Tasks**: Run `/sp.tasks` to create tasks.md with:
   - Task 1: Implement Task entity (domain/task.py)
   - Task 2: Implement TaskService (application/task_service.py)
   - Task 3: Implement CLI (infrastructure/cli.py)
   - Task 4: Implement main entry point (main.py)
   - Task 5-8: Unit tests for each module
   - Task 9: Integration tests for full workflows
3. **Implementation**: Run `/sp.implement` following TDD (Red-Green-Refactor)

**Files to Generate Next** (by /sp.tasks):
- Source: `src/domain/task.py`, `src/application/task_service.py`, `src/infrastructure/cli.py`, `src/main.py`
- Tests: `tests/unit/test_task.py`, `tests/unit/test_task_service.py`, `tests/integration/test_cli_integration.py`
