# Data Model: Phase I Console Todo

**Feature**: Phase I Console Todo
**Date**: 2025-12-28
**Phase**: 1 (Design)

## Entities

### Task

Represents a single todo item with unique identifier, description, and completion status.

#### Attributes

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| `id` | int | Unique, sequential, > 0 | Auto-assigned | Unique identifier for the task, starting from 1 |
| `description` | str | Min 1 char (after strip), no max | Required | Text describing what needs to be done |
| `is_complete` | bool | True or False | False | Completion status (False = Incomplete, True = Complete) |

#### Validation Rules

1. **ID Validation**:
   - Auto-assigned by TaskService starting from 1
   - Sequential increment: each new task gets `previous_id + 1`
   - Never reused after deletion (SC-006)
   - Must be positive integer

2. **Description Validation** (FR-002):
   - Must not be empty after stripping whitespace
   - Whitespace-only strings are invalid
   - No maximum length (system accepts long descriptions per edge case)
   - Unicode characters supported

3. **Status Validation**:
   - Boolean field: True (Complete) or False (Incomplete)
   - Default is False (Incomplete) per FR-005
   - Can be toggled between True and False (FR-009)

#### State Transitions

**Task Status Lifecycle**:

```
[Created]
   ↓
Incomplete (is_complete=False) ←→ Complete (is_complete=True)
   ↑                                       ↑
   └───────────────────┬───────────────────┘
                       ↓
                  [Deleted]
```

**Valid Transitions**:
- Create → Incomplete (initial state per FR-005)
- Incomplete → Complete (mark complete)
- Complete → Incomplete (mark incomplete)
- Any state → Deleted (delete task)

**Invalid Transitions**: None (all transitions allowed)

#### Python Implementation

```python
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique sequential integer identifier (auto-assigned)
        description: Text describing the task (min 1 char after strip)
        is_complete: Completion status (False = Incomplete, True = Complete)
    """
    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """Validate task attributes."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        if not isinstance(self.description, str):
            raise ValueError("Task description must be a string")

        # Strip and validate description
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("Task description cannot be empty")

        if not isinstance(self.is_complete, bool):
            raise ValueError("Task status must be a boolean")

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.is_complete = False

    def toggle_status(self) -> None:
        """Toggle task completion status."""
        self.is_complete = not self.is_complete

    def get_status_display(self) -> str:
        """Get human-readable status string."""
        return "Complete" if self.is_complete else "Incomplete"
```

## Relationships

**Phase I**: No relationships (single entity system)

Future phases may introduce:
- Phase II: Task → Category (one-to-many)
- Phase II: Task → Tag (many-to-many)
- Phase III: Task → User (many-to-one)

## Storage Strategy

**Phase I**: In-memory dictionary

```python
# In TaskService
tasks: dict[int, Task] = {}
next_id: int = 1
```

**Key**: Task ID (integer)
**Value**: Task instance

**Rationale**:
- O(1) lookups by ID (FR-010 validation)
- O(1) insert/delete operations
- No persistence required (FR-012, FR-014)
- Simple, no external dependencies

**Memory Footprint**:
- Estimated 96 bytes per task (id + description + status + dict overhead)
- 100 tasks ≈ 10 KB (well within limits per SC-008)

## Data Constraints

### Functional Constraints (from spec.md)

- **FR-002**: Description minimum 1 character after trimming whitespace
- **FR-003**: IDs must be unique, sequential, starting from 1
- **FR-004**: Task must have exactly three attributes (id, description, status)
- **FR-005**: New tasks default to Incomplete status
- **FR-012**: All data stored in memory only (no files, no databases)
- **FR-014**: All data cleared when application exits

### Performance Constraints (from spec.md)

- **SC-001**: Task creation within 5 seconds
- **SC-002**: Task list retrieval within 2 seconds
- **SC-006**: IDs remain unique throughout session (no reuse after delete)
- **SC-008**: Support 100+ tasks without performance degradation

## Edge Cases

1. **Long descriptions** (1000+ characters):
   - System accepts and stores full description
   - Display may truncate for readability in CLI

2. **Special characters and unicode**:
   - System accepts all valid UTF-8 characters
   - Terminal must support UTF-8 encoding (assumption #9)

3. **Task ID overflow** (beyond 999):
   - Python int has unlimited precision
   - System continues assigning sequential IDs without limit

4. **Empty task list**:
   - Valid state (initial state when app launches)
   - Operations handle gracefully (return empty list, show "No tasks found")

5. **Deleted task IDs**:
   - IDs never reused (SC-006)
   - Dict storage allows gaps in ID sequence

## Data Model Evolution

**Phase I → Phase II**:
- Add optional fields: `category`, `deadline`, `recurring`
- Maintain backward compatibility: new fields optional with defaults

**Phase II → Phase III**:
- Add `user_id` foreign key
- Add `created_at`, `updated_at` timestamps
- Migration strategy: export Phase II data, import to Phase III database

**Phase III → Phase IV/V**:
- Add `priority`, `tags`, `attachments`
- Implement event sourcing for audit trail
- Scale to distributed storage (PostgreSQL → Neon DB)
