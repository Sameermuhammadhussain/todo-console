# Quickstart Guide: Phase I Console Todo

**Feature**: Phase I Console Todo
**Date**: 2025-12-28
**Target Users**: Developers implementing and testing Phase I

## Prerequisites

- **Python**: 3.11 or higher
- **pytest**: For running tests (install via `pip install pytest pytest-cov`)
- **Operating System**: Windows, Linux, or macOS
- **Terminal**: UTF-8 encoding support for international characters

## Project Structure

```text
todo-console/
├── src/
│   ├── domain/
│   │   └── task.py              # Task entity
│   ├── application/
│   │   └── task_service.py      # Task operations
│   ├── infrastructure/
│   │   └── cli.py               # Console interface
│   └── main.py                  # Application entry point
├── tests/
│   ├── unit/
│   │   ├── test_task.py         # Task entity tests
│   │   └── test_task_service.py # TaskService tests
│   └── integration/
│       └── test_cli_integration.py # End-to-end tests
└── specs/
    └── 001-phase1-console-todo/
        ├── spec.md              # Feature specification
        ├── plan.md              # Implementation plan
        ├── data-model.md        # Entity definitions
        ├── quickstart.md        # This file
        └── contracts/
            └── task_operations.md # TaskService interface
```

## Installation

### 1. Clone Repository (if applicable)

```bash
git clone <repository-url>
cd todo-console
```

### 2. Install Dependencies

**Testing dependencies only** (application has no runtime dependencies):

```bash
pip install pytest pytest-cov
```

Or using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install pytest pytest-cov
```

### 3. Verify Installation

```bash
python --version  # Should be 3.11+
pytest --version  # Should be 7.0+
```

## Running the Application

### Launch Console Application

```bash
python src/main.py
```

**Expected Output**:
```
=== Todo List Manager ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter choice:
```

### Basic Usage Flow

1. **Add a task**:
   - Choose option `1`
   - Enter task description: `Buy groceries`
   - System displays: `Task added with ID 1`

2. **View tasks**:
   - Choose option `2`
   - System displays task list:
     ```
     ID  | Description          | Status
     ----|---------------------|----------
     1   | Buy groceries       | Incomplete
     ```

3. **Mark task complete**:
   - Choose option `5`
   - Enter task ID: `1`
   - System displays: `Task 1 marked as complete`

4. **Update task**:
   - Choose option `3`
   - Enter task ID: `1`
   - Enter new description: `Buy organic groceries`
   - System displays: `Task 1 updated successfully`

5. **Delete task**:
   - Choose option `4`
   - Enter task ID: `1`
   - System displays: `Task 1 deleted successfully`

6. **Exit application**:
   - Choose option `7`
   - System displays: `Goodbye!`
   - Application terminates (all data cleared)

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

**Expected Output**:
```
tests/unit/test_task.py::test_task_creation PASSED
tests/unit/test_task.py::test_task_validation PASSED
tests/unit/test_task_service.py::test_add_task_success PASSED
tests/unit/test_task_service.py::test_add_task_empty_description PASSED
...
==================== X passed in Y.YYs ====================
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Expected Coverage**: 80%+ (target per constitution)

**Sample Output**:
```
---------- coverage: platform windows, python 3.11.x -----------
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
src\domain\task.py                     20      0   100%
src\application\task_service.py        45      2    96%   78-79
src\infrastructure\cli.py              60     12    80%   45-50, 89-92
src\main.py                             5      0   100%
-----------------------------------------------------------------
TOTAL                                 130     14    89%
```

### Run Specific Test Files

**Unit tests only**:
```bash
pytest tests/unit/ -v
```

**Integration tests only**:
```bash
pytest tests/integration/ -v
```

**Specific test function**:
```bash
pytest tests/unit/test_task_service.py::test_add_task_success -v
```

### Generate HTML Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

Open `htmlcov/index.html` in browser to view detailed coverage report.

## Development Workflow

### 1. Implement a Module

Follow TDD (Red-Green-Refactor):

**Red - Write failing test**:
```python
# tests/unit/test_task.py
def test_task_creation():
    task = Task(id=1, description="Test task", is_complete=False)
    assert task.id == 1
    assert task.description == "Test task"
    assert task.is_complete == False
```

Run test (should fail):
```bash
pytest tests/unit/test_task.py::test_task_creation
```

**Green - Implement minimum code**:
```python
# src/domain/task.py
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    description: str
    is_complete: bool = False
```

Run test (should pass):
```bash
pytest tests/unit/test_task.py::test_task_creation
```

**Refactor - Improve code quality**:
```python
# Add validation, docstrings, type hints
```

Run tests again to ensure nothing broke.

### 2. Verify Constitution Compliance

Before committing, check:
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ No Phase II+ features introduced
- ✅ Clean architecture maintained (domain/application/infrastructure)
- ✅ No external dependencies (except pytest for testing)

### 3. Run Full Test Suite

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

Expected: All tests pass, coverage ≥ 80%

## Troubleshooting

### Issue: ModuleNotFoundError

**Symptom**:
```
ModuleNotFoundError: No module named 'src'
```

**Solution**:
Run from repository root:
```bash
cd /path/to/todo-console
python src/main.py
```

Or add `src/` to PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"  # Linux/macOS
set PYTHONPATH=%PYTHONPATH%;%cd%\src          # Windows
```

### Issue: Tests Not Found

**Symptom**:
```
collected 0 items
```

**Solution**:
Ensure `__init__.py` files exist in test directories:
```bash
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

### Issue: pytest Not Installed

**Symptom**:
```
'pytest' is not recognized as an internal or external command
```

**Solution**:
Install pytest:
```bash
pip install pytest pytest-cov
```

### Issue: UnicodeEncodeError

**Symptom**:
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution** (Windows):
Set UTF-8 encoding:
```bash
set PYTHONIOENCODING=utf-8
python src/main.py
```

Or configure terminal to use UTF-8 encoding.

## Performance Benchmarks

**Target** (from spec.md Success Criteria):
- SC-001: Add task within 5 seconds
- SC-002: View tasks within 2 seconds
- SC-008: Support 100+ tasks without degradation

**Expected Actual**:
- Add task: < 0.1 seconds (O(1) dict insert)
- View tasks: < 0.1 seconds for 100 tasks (O(n log n) sort)
- Update/Delete/Toggle: < 0.1 seconds (O(1) dict operations)

**Verify Performance**:
```python
# Add 100 tasks and measure
import time

service = TaskService()
start = time.time()
for i in range(100):
    service.add_task(f"Task {i}")
elapsed = time.time() - start
print(f"Added 100 tasks in {elapsed:.3f} seconds")  # Should be < 1 second

start = time.time()
tasks = service.list_tasks()
elapsed = time.time() - start
print(f"Listed 100 tasks in {elapsed:.3f} seconds")  # Should be < 1 second
```

## Next Steps

After verifying Phase I implementation:

1. **Review**: Ensure all acceptance criteria from spec.md are met
2. **Generate Tasks**: Run `/sp.tasks` to create detailed task breakdown
3. **Implementation**: Follow tasks.md using TDD workflow
4. **Testing**: Achieve 80%+ coverage
5. **Documentation**: Update this quickstart if usage patterns change
6. **Commit**: Use `/sp.git.commit_pr` to create PR

## References

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **TaskService Contract**: [contracts/task_operations.md](./contracts/task_operations.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
