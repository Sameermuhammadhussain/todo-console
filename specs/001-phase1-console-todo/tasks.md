# Tasks: Phase I Console Todo

**Input**: Design documents from `/specs/001-phase1-console-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/task_operations.md

**Tests**: Following TDD (Test-Driven Development) - Tests are written FIRST and must FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow clean architecture: `src/domain/`, `src/application/`, `src/infrastructure/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure per plan.md

- [x] T001 Create project directory structure with src/domain/, src/application/, src/infrastructure/, tests/unit/, tests/integration/
- [x] T002 Create empty __init__.py files in src/, src/domain/, src/application/, src/infrastructure/, tests/, tests/unit/, tests/integration/
- [x] T003 [P] Create pytest.ini configuration file with test paths and coverage settings
- [x] T004 [P] Create .gitignore for Python project (__pycache__/, *.pyc, .pytest_cache/, htmlcov/)

**Checkpoint**: Project structure ready - domain layer implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task entity that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Write unit test for Task entity creation in tests/unit/test_task.py (must FAIL initially)
- [x] T006 [P] Write unit test for Task entity validation (empty description, invalid ID) in tests/unit/test_task.py (must FAIL initially)
- [x] T007 Implement Task entity as dataclass in src/domain/task.py (id: int, description: str, is_complete: bool = False)
- [x] T008 Add __post_init__ validation to Task entity in src/domain/task.py (validate id > 0, description non-empty after strip)
- [x] T009 Add helper methods to Task entity in src/domain/task.py (mark_complete, mark_incomplete, toggle_status, get_status_display)
- [x] T010 Run pytest tests/unit/test_task.py to verify all Task entity tests pass

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Implement core MVP functionality - users can add tasks and view their task list

**Independent Test**: Launch application, add 3 tasks with different descriptions, view list showing all tasks with IDs and status

**Spec Reference**: spec.md lines 10-24 (User Story 1 acceptance scenarios)
**Plan Reference**: plan.md lines 223-269 (TaskService contract for add_task and list_tasks)

### Tests for User Story 1 (TDD - Write FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Write unit test for TaskService.add_task() success case in tests/unit/test_task_service.py (must FAIL initially)
- [x] T012 [P] [US1] Write unit test for TaskService.add_task() with empty description in tests/unit/test_task_service.py (must FAIL initially)
- [x] T013 [P] [US1] Write unit test for TaskService.list_tasks() with empty list in tests/unit/test_task_service.py (must FAIL initially)
- [x] T014 [P] [US1] Write unit test for TaskService.list_tasks() with multiple tasks in tests/unit/test_task_service.py (must FAIL initially)
- [x] T015 [P] [US1] Write integration test for add task flow in tests/integration/test_cli_integration.py (must FAIL initially)
- [x] T016 [P] [US1] Write integration test for view tasks flow in tests/integration/test_cli_integration.py (must FAIL initially)

### Implementation for User Story 1

- [x] T017 [US1] Implement TaskService.__init__ with tasks dict and next_id counter in src/application/task_service.py
- [x] T018 [US1] Implement TaskService.add_task() method in src/application/task_service.py (validate description, assign ID, store task, return Task or error string per contract)
- [x] T019 [US1] Implement TaskService.get_task() helper method in src/application/task_service.py (lookup by ID, return Task or None)
- [x] T020 [US1] Implement TaskService.list_tasks() method in src/application/task_service.py (return all tasks sorted by ID)
- [x] T021 [US1] Run pytest tests/unit/test_task_service.py::test_add_task* to verify add_task tests pass
- [x] T022 [US1] Run pytest tests/unit/test_task_service.py::test_list_tasks* to verify list_tasks tests pass
- [x] T023 [US1] Implement CLI menu display function in src/infrastructure/cli.py (show 7 options: Add, View, Update, Delete, Mark Complete, Mark Incomplete, Exit)
- [x] T024 [US1] Implement CLI main loop in src/infrastructure/cli.py (display menu, read choice, dispatch to handlers, repeat until exit)
- [x] T025 [US1] Implement handle_add_task() in src/infrastructure/cli.py (prompt for description, call service.add_task, display success/error message)
- [x] T026 [US1] Implement handle_view_tasks() in src/infrastructure/cli.py (call service.list_tasks, display table or "No tasks found" message)
- [x] T027 [US1] Implement main entry point in src/main.py (initialize TaskService, launch CLI loop)
- [x] T028 [US1] Run pytest tests/integration/test_cli_integration.py to verify User Story 1 integration tests pass

**Checkpoint**: MVP complete - users can add and view tasks. Application is minimally functional and can be demonstrated.

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Add task state management - users can mark tasks as complete or incomplete

**Independent Test**: Add 3 tasks, mark task 2 complete, mark task 1 complete, mark task 2 incomplete, view list verifying status changes

**Spec Reference**: spec.md lines 27-41 (User Story 2 acceptance scenarios)
**Plan Reference**: plan.md lines 265-269 (TaskService contract for toggle_complete)

### Tests for User Story 2 (TDD - Write FIRST)

- [x] T029 [P] [US2] Write unit test for TaskService.toggle_complete() success case in tests/unit/test_task_service.py (must FAIL initially)
- [x] T030 [P] [US2] Write unit test for TaskService.toggle_complete() with invalid ID in tests/unit/test_task_service.py (must FAIL initially)
- [x] T031 [P] [US2] Write unit test for TaskService.toggle_complete() round-trip (toggle twice) in tests/unit/test_task_service.py (must FAIL initially)
- [x] T032 [P] [US2] Write integration test for mark complete flow in tests/integration/test_cli_integration.py (must FAIL initially)
- [x] T033 [P] [US2] Write integration test for mark incomplete flow in tests/integration/test_cli_integration.py (must FAIL initially)

### Implementation for User Story 2

- [x] T034 [US2] Implement TaskService.toggle_complete() method in src/application/task_service.py (validate ID exists, toggle is_complete, return True or error string)
- [x] T035 [US2] Run pytest tests/unit/test_task_service.py::test_toggle_complete* to verify toggle_complete tests pass
- [x] T036 [US2] Implement handle_mark_complete() in src/infrastructure/cli.py (check tasks exist, prompt for ID, parse integer, call service.toggle_complete, display success/error)
- [x] T037 [US2] Implement handle_mark_incomplete() in src/infrastructure/cli.py (reuse toggle_complete logic, same flow as mark complete)
- [x] T038 [US2] Add error handling for non-numeric ID input in src/infrastructure/cli.py (catch ValueError, display "Please enter a valid number")
- [x] T039 [US2] Run pytest tests/integration/test_cli_integration.py to verify User Story 2 integration tests pass

**Checkpoint**: User Stories 1 AND 2 functional - users can add, view, and mark tasks complete/incomplete

---

## Phase 5: User Story 3 - Update Task Description (Priority: P3)

**Goal**: Add task editing capability - users can update task descriptions

**Independent Test**: Add task "Buy milk", update to "Buy organic milk", view list verifying description changed

**Spec Reference**: spec.md lines 44-58 (User Story 3 acceptance scenarios)
**Plan Reference**: plan.md lines 256-264 (TaskService contract for update_task)

### Tests for User Story 3 (TDD - Write FIRST)

- [x] T040 [P] [US3] Write unit test for TaskService.update_task() success case in tests/unit/test_task_service.py (must FAIL initially)
- [x] T041 [P] [US3] Write unit test for TaskService.update_task() with invalid ID in tests/unit/test_task_service.py (must FAIL initially)
- [x] T042 [P] [US3] Write unit test for TaskService.update_task() with empty description in tests/unit/test_task_service.py (must FAIL initially)
- [x] T043 [P] [US3] Write integration test for update task flow in tests/integration/test_cli_integration.py (must FAIL initially)

### Implementation for User Story 3

- [x] T044 [US3] Implement TaskService.update_task() method in src/application/task_service.py (validate ID exists, validate new description non-empty, update description, return True or error string)
- [x] T045 [US3] Run pytest tests/unit/test_task_service.py::test_update_task* to verify update_task tests pass
- [x] T046 [US3] Implement handle_update_task() in src/infrastructure/cli.py (check tasks exist, prompt for ID, parse integer, prompt for new description, call service.update_task, display success/error)
- [x] T047 [US3] Run pytest tests/integration/test_cli_integration.py to verify User Story 3 integration tests pass

**Checkpoint**: User Stories 1, 2, AND 3 functional - users can add, view, update, and mark tasks complete/incomplete

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Add task removal capability - users can delete unwanted tasks

**Independent Test**: Add 5 tasks, delete task 3, view list verifying task 3 removed and IDs not reused, delete task 1, add new task verifying ID continues sequentially

**Spec Reference**: spec.md lines 61-75 (User Story 4 acceptance scenarios)
**Plan Reference**: plan.md lines 260-264 (TaskService contract for delete_task)

### Tests for User Story 4 (TDD - Write FIRST)

- [x] T048 [P] [US4] Write unit test for TaskService.delete_task() success case in tests/unit/test_task_service.py (must FAIL initially)
- [x] T049 [P] [US4] Write unit test for TaskService.delete_task() with invalid ID in tests/unit/test_task_service.py (must FAIL initially)
- [x] T050 [P] [US4] Write unit test for TaskService.delete_task() ID not reused in tests/unit/test_task_service.py (must FAIL initially)
- [x] T051 [P] [US4] Write integration test for delete task flow in tests/integration/test_cli_integration.py (must FAIL initially)

### Implementation for User Story 4

- [x] T052 [US4] Implement TaskService.delete_task() method in src/application/task_service.py (validate ID exists, delete from dict, do NOT decrement next_id, return True or error string)
- [x] T053 [US4] Run pytest tests/unit/test_task_service.py::test_delete_task* to verify delete_task tests pass
- [x] T054 [US4] Implement handle_delete_task() in src/infrastructure/cli.py (check tasks exist, prompt for ID, parse integer, call service.delete_task, display success/error)
- [x] T055 [US4] Run pytest tests/integration/test_cli_integration.py to verify User Story 4 integration tests pass

**Checkpoint**: All user stories complete - users can add, view, update, delete, and mark tasks complete/incomplete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finalize error handling, validation, and ensure all acceptance criteria met

- [x] T056 [P] Add input validation for menu choice in src/infrastructure/cli.py (display "Invalid choice. Please enter 1-7" for invalid choices)
- [x] T057 [P] Verify all error messages match spec.md FR-011 requirements (empty description, task not found, no tasks available, invalid choice, non-numeric ID)
- [x] T058 [P] Add "No tasks available" check before operations that require tasks in src/infrastructure/cli.py (update, delete, mark complete/incomplete)
- [x] T059 Run full test suite with coverage: pytest tests/ -v --cov=src --cov-report=term-missing
- [x] T060 Verify coverage >= 80% per constitution requirement (if below, add missing tests)
- [x] T061 Manual testing: Follow quickstart.md usage flows to verify all acceptance scenarios from spec.md
- [x] T062 Verify application exits cleanly and memory cleared per FR-014 (no persistence after exit)
- [x] T063 [P] Performance test: Add 100 tasks, verify operations complete within SC-001/SC-002 time limits (5s add, 2s view)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3 → P4)
  - Each story is independently testable after completion
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Requires US1 completed (needs add/view to test mark complete)
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) - Requires US1 completed (needs add/view to test update)
- **User Story 4 (P4)**: Depends on Foundational (Phase 2) - Requires US1 completed (needs add/view to test delete)

### Within Each User Story

- **TDD Workflow**: Tests written FIRST → Tests FAIL → Implementation → Tests PASS
- Tests before implementation (all test tasks can run in parallel within a story)
- Domain/Application layer before Infrastructure layer
- Service methods before CLI handlers
- Unit tests pass before integration tests
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T001 must complete first, then T002-T004 can run in parallel
- **Phase 2 (Foundational)**: T005-T006 (tests) can run in parallel, T007-T009 sequential, T010 final verification
- **Within Each User Story**:
  - All test tasks marked [P] can run in parallel
  - Service implementation is sequential (depends on tests)
  - CLI handlers depend on service methods
- **Phase 7 (Polish)**: T056-T058, T063 can run in parallel, T059-T062 sequential verification

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T011: Write unit test for TaskService.add_task() success
Task T012: Write unit test for TaskService.add_task() with empty description
Task T013: Write unit test for TaskService.list_tasks() with empty list
Task T014: Write unit test for TaskService.list_tasks() with multiple tasks
Task T015: Write integration test for add task flow
Task T016: Write integration test for view tasks flow

# After tests written, implementation is sequential:
T017 → T018 → T019 → T020 → Verify tests pass → T023 → T024 → T025 → T026 → T027 → T028
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T010) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T011-T028)
4. **STOP and VALIDATE**: Test User Story 1 independently per quickstart.md
5. Demonstrate MVP: Add tasks, view tasks, verify persistence isolation

**Deliverable**: Working console app with add/view functionality

### Incremental Delivery

1. **Foundation**: Setup + Foundational (T001-T010) → Project structure ready
2. **MVP**: Add User Story 1 (T011-T028) → Test independently → **Deploy/Demo**
3. **Increment 2**: Add User Story 2 (T029-T039) → Test independently → **Deploy/Demo**
4. **Increment 3**: Add User Story 3 (T040-T047) → Test independently → **Deploy/Demo**
5. **Increment 4**: Add User Story 4 (T048-T055) → Test independently → **Deploy/Demo**
6. **Polish**: Phase 7 (T056-T063) → Final validation → **Release**

Each increment adds value without breaking previous functionality.

### Sequential Execution (Single Developer)

Recommended order:
- Phase 1 (Setup): T001 → T002 → [T003, T004 parallel]
- Phase 2 (Foundational): [T005, T006 parallel] → T007 → T008 → T009 → T010
- Phase 3 (US1): [T011-T016 parallel tests] → T017 → T018 → T019 → T020 → T021 → T022 → T023 → T024 → T025 → T026 → T027 → T028
- Phase 4 (US2): [T029-T033 parallel tests] → T034 → T035 → T036 → T037 → T038 → T039
- Phase 5 (US3): [T040-T043 parallel tests] → T044 → T045 → T046 → T047
- Phase 6 (US4): [T048-T051 parallel tests] → T052 → T053 → T054 → T055
- Phase 7 (Polish): [T056, T057, T058, T063 parallel] → T059 → T060 → T061 → T062

**Total Estimated Time**: 1-2 days for experienced developer following TDD

---

## Task Acceptance Criteria

### Every Task Must:
- [ ] Be completable independently (once preconditions met)
- [ ] Produce verifiable output (code, tests passing, file created)
- [ ] Follow clean architecture principles (correct layer for artifact)
- [ ] Not introduce Phase II+ features
- [ ] Include explicit file path in description

### Test Tasks Must:
- [ ] Write test BEFORE implementation
- [ ] Verify test FAILS initially (Red in TDD)
- [ ] Cover success case and error cases
- [ ] Follow pytest conventions

### Implementation Tasks Must:
- [ ] Make previously failing tests PASS (Green in TDD)
- [ ] Follow contracts defined in contracts/task_operations.md
- [ ] Include error handling per spec.md FR-011
- [ ] Maintain constitution compliance (clean architecture, no external dependencies)

---

## Notes

- **TDD Required**: All tests written FIRST and must FAIL before implementation begins
- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Each user story**: Independently completable and testable after its phase
- **Verify tests fail**: Before implementing, run pytest and confirm RED state
- **Commit frequency**: After each task or logical group of related tasks
- **Stop at checkpoints**: Validate story independently before proceeding
- **Constitution compliance**: 80% test coverage, clean architecture, no external dependencies, Phase I scope only

**Key Files Referenced**:
- **spec.md**: User stories (lines 10-75), functional requirements (lines 86-105)
- **plan.md**: Architecture (lines 60-76), project structure (lines 95-111), TaskService contract (lines 223-269)
- **data-model.md**: Task entity specification, validation rules
- **contracts/task_operations.md**: Complete TaskService interface, error handling strategy
- **quickstart.md**: Testing commands, usage flows, troubleshooting
