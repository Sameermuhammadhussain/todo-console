---
id: 002
title: Phase I technical plan
stage: plan
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 001-phase1-console-todo
branch: 001-phase1-console-todo
user: ESHOP
command: /sp.plan
labels: ["planning", "architecture", "clean-architecture", "phase1", "in-memory"]
links:
  spec: specs/001-phase1-console-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase1-console-todo/plan.md
  - specs/001-phase1-console-todo/research.md
  - specs/001-phase1-console-todo/data-model.md
  - specs/001-phase1-console-todo/quickstart.md
  - specs/001-phase1-console-todo/contracts/task_operations.md
tests:
  - N/A
---

## Prompt

```
Create the Phase I technical plan for the Todo in-memory Python console application.

The plan must be derived strictly from the Phase I specification and global constitution.

Include:
1. High-level application structure (single Python program)
2. In-memory data structures to store tasks
3. Task identification strategy (ID generation)
4. CLI control flow (menu loop, user input handling)
5. Separation of responsibilities (data handling vs CLI)
6. Error handling strategy for invalid input and missing tasks

Constraints:
- No databases
- No file storage
- No web frameworks
- No external services
- No future phase concepts

The plan must not introduce new features.
It must only describe HOW the approved Phase I requirements will be implemented.
```

## Response snapshot

Created comprehensive Phase I technical plan with clean architecture design.

**Architecture**: Three-layer clean architecture
- **Domain Layer**: Task entity (id, description, is_complete) with validation
- **Application Layer**: TaskService with 6 operations (add, get, list, update, delete, toggle_complete)
- **Infrastructure Layer**: CLI menu loop with input/output handling

**Key Decisions**:
1. **Layered Architecture**: Clean architecture despite Phase I simplicity - mandated by constitution Principle V, prepares for Phase III web migration
2. **Storage**: Python dict keyed by integer task ID - O(1) operations, meets performance requirements (SC-001: 5s add, SC-002: 2s view)
3. **ID Generation**: Sequential counter starting at 1, never reused after delete (meets SC-006)
4. **Error Handling**: Return error strings vs raising exceptions - user errors expected/recoverable

**Project Structure**:
```
src/
├── domain/task.py           # Task entity dataclass
├── application/task_service.py  # CRUD + toggle operations
├── infrastructure/cli.py    # Menu loop, input validation
└── main.py                  # Entry point

tests/
├── unit/                    # 100% coverage for domain/application
└── integration/             # End-to-end CLI workflows
```

**Supporting Documents Created**:
1. **research.md**: Python console patterns, dict vs list analysis, pytest strategies
2. **data-model.md**: Task entity definition, validation rules, state transitions, storage strategy
3. **contracts/task_operations.md**: TaskService interface with all 6 methods, error handling contract, performance guarantees
4. **quickstart.md**: Setup instructions, usage flows, testing commands, troubleshooting

**Constitution Compliance**:
- ✅ Spec-Driven Development: Plan derived strictly from spec.md
- ✅ Phase Governance: No Phase II+ features (categories, deadlines, persistence)
- ✅ Technology Constraints: Python 3.11+, pytest only, no external dependencies
- ✅ Clean Architecture: Domain/application/infrastructure separation enforced
- ✅ Testing: 80%+ coverage target, TDD workflow defined

**Architectural Decision Detected**:
📋 Clean Architecture layering for Phase I console app - mandates separate domain/application/infrastructure layers despite simple CRUD scope. Rationale: Constitution Principle V requires clean architecture; prepares codebase for Phase III FastAPI migration. Trade-off: More files/complexity now vs easier evolution later.

## Outcome

- ✅ Impact: Complete technical plan ready for task generation
- 🧪 Tests: Testing strategy defined (pytest, monkeypatch, 80% coverage target)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/task_operations.md (5 artifacts)
- 🔁 Next prompts: Document ADR with `/sp.adr clean-architecture-phase1`, then run `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Plan successfully translates WHAT (spec) to HOW (implementation approach) while maintaining strict Phase I boundaries and constitution compliance. Architecture decisions explicitly documented with rationale and trade-offs.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 5 principles verified)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Monitor during implementation whether clean architecture overhead (3 layers for simple CRUD) creates unnecessary friction or aids testability/evolution as intended
