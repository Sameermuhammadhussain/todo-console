# Evolution of Todo Project Constitution

<!--
Sync Impact Report:
Version change: [initial] → 1.0.0
Modified principles: Initial creation
Added sections:
  - I. Spec-Driven Development (Mandatory)
  - II. Agent Behavior Rules
  - III. Phase Governance
  - IV. Technology Constraints
  - V. Quality & Architecture Principles
  - Technology Stack
  - Development Workflow
  - Governance
Removed sections: None
Templates requiring updates:
  ✅ plan-template.md - reviewed
  ✅ spec-template.md - reviewed
  ✅ tasks-template.md - reviewed
  ✅ commands/*.md - reviewed
Follow-up TODOs: None
-->

## Core Principles

### I. Spec-Driven Development (Mandatory)

**No agent may write code without approved specifications and tasks.**

All work MUST follow the strict sequence:
1. **Constitution** → Review and ensure compliance with project principles
2. **Specification** → Define requirements, acceptance criteria, and scope
3. **Plan** → Architecture decisions, design, and approach
4. **Tasks** → Testable, atomic work items with acceptance criteria
5. **Implement** → Execute tasks following TDD (Red-Green-Refactor)

**Rationale**: Spec-Driven Development ensures that all work is intentional, traceable, and aligned with user intent. It prevents scope creep, maintains architectural coherence across phases, and enables validation before resource investment.

**Non-negotiable rules**:
- No coding begins until spec.md, plan.md, and tasks.md exist and are approved
- All changes to functionality require spec updates first
- Refinement occurs at spec level, never at code level
- Specs act as living documentation and contracts between phases

### II. Agent Behavior Rules

**Agents are executors of approved specifications, not autonomous inventors.**

MUST behaviors:
- Execute only approved tasks from tasks.md
- Follow specifications exactly as written
- Request clarification when ambiguity exists
- Document all architectural decisions in ADRs
- Create Prompt History Records (PHRs) for every interaction
- Suggest ADRs for architecturally significant decisions

MUST NOT behaviors:
- Invent features not in approved specs
- Deviate from approved specifications
- Make architectural decisions without user consent
- Manually write code without approved tasks
- Skip or modify the Spec-Driven Development workflow
- Implement future-phase features prematurely

**Rationale**: Strict agent behavior ensures predictability, traceability, and alignment with project goals. Human judgment remains paramount for strategic decisions while agents provide consistent execution.

### III. Phase Governance

**Each phase is strictly scoped; no feature leakage across phases.**

Phase boundaries:
- **Phase I**: Console-based Todo CRUD (Python CLI)
- **Phase II**: Advanced features (categories, deadlines, recurring)
- **Phase III**: Multi-user web application (Next.js frontend, FastAPI backend)
- **Phase IV**: Multi-agent collaboration (OpenAI Agents SDK, MCP)
- **Phase V**: Enterprise scale (Kubernetes, Kafka, Dapr, distributed systems)

Phase rules:
- Each phase has its own dedicated specification
- Features from Phase N+1 MUST NOT appear in Phase N
- Architecture may evolve between phases ONLY through updated specs and plans
- Backward compatibility is required when phases depend on earlier components
- Each phase must be completable, testable, and deployable independently

**Rationale**: Phase boundaries prevent premature optimization, maintain focus, and ensure each phase delivers value independently. Clear separation enables incremental learning and controlled complexity growth.

### IV. Technology Constraints

**Technology stack is prescribed; deviations require constitutional amendment.**

**Backend (All Phases)**:
- Language: Python 3.11+
- Framework: FastAPI (Phase III+)
- ORM: SQLModel
- Database: Neon DB (PostgreSQL-compatible)
- Testing: pytest

**Frontend (Phase III+)**:
- Framework: Next.js (React)
- Language: TypeScript
- State Management: TBD in Phase III spec
- UI Library: TBD in Phase III spec

**AI & Integration (Phase IV+)**:
- Agent Framework: OpenAI Agents SDK
- Protocol: Model Context Protocol (MCP)

**Infrastructure (Phase V+)**:
- Containerization: Docker
- Orchestration: Kubernetes
- Event Streaming: Apache Kafka
- Service Mesh: Dapr

**Allowed additions**:
- Supporting libraries that align with stack choices (e.g., Pydantic, SQLAlchemy extensions)
- Testing/development tools (e.g., Black, Ruff, ESLint)

**Prohibited**:
- Alternative frameworks/languages not listed above
- Technology replacements without constitutional amendment
- Experimental or unstable dependencies in production

**Rationale**: Technology constraints ensure consistency, reduce decision fatigue, enable cumulative expertise, and simplify integration across phases.

### V. Quality & Architecture Principles

**Clean architecture, stateless services, and cloud-native readiness are non-negotiable.**

**Clean Architecture**:
- Clear separation of concerns (domain, application, infrastructure layers)
- Domain logic isolated from frameworks and external dependencies
- Dependency inversion: high-level modules do not depend on low-level modules
- Explicit boundaries between layers enforced through interfaces

**Stateless Services (Phase III+)**:
- Services MUST NOT maintain user session state in memory
- All state persisted to database or cache layer
- Horizontal scalability required for all backend services
- No server affinity/sticky sessions

**Separation of Concerns**:
- Single Responsibility Principle (SRP) at all levels
- No business logic in UI components or HTTP handlers
- Configuration externalized (environment variables, config files)
- Clear module boundaries with defined public APIs

**Cloud-Native Readiness**:
- 12-Factor App principles followed
- Health checks and readiness probes implemented
- Graceful shutdown and startup
- Logging to stdout/stderr, metrics exposed for collection
- Secrets management through external providers (not hardcoded)

**Testing discipline**:
- Unit tests for all business logic
- Integration tests for cross-boundary interactions
- End-to-end tests for critical user flows
- Minimum 80% code coverage (domain and application layers)

**Rationale**: These principles ensure maintainability, scalability, and operational excellence as the project evolves from console app to enterprise distributed system.

## Technology Stack

**See Principle IV (Technology Constraints) for the complete prescribed stack.**

Key stack decisions and rationale:
- **Python**: Rich ecosystem, AI/ML integration, FastAPI performance
- **FastAPI**: Modern async framework, automatic OpenAPI docs, high performance
- **SQLModel**: Type-safe ORM combining SQLAlchemy and Pydantic
- **Neon DB**: Serverless PostgreSQL, branching support, cost-effective scaling
- **Next.js**: React framework with SSR/SSG, excellent DX, production-ready
- **OpenAI Agents SDK**: First-class agent support, MCP integration
- **Kubernetes + Kafka + Dapr**: Industry-standard enterprise patterns

## Development Workflow

**All development follows Spec-Driven Development (see Principle I).**

### Standard workflow sequence:

1. **Constitution Review**: Ensure work aligns with project principles
2. **Specification (`/sp.specify`)**: Create or update feature spec.md
   - User provides natural language requirements
   - Agent generates structured specification
   - User approves specification
3. **Planning (`/sp.plan`)**: Generate architectural plan.md
   - Agent explores codebase and designs approach
   - Identifies architectural decisions
   - User approves plan
4. **Task Generation (`/sp.tasks`)**: Create actionable tasks.md
   - Agent breaks plan into testable tasks
   - Dependencies and acceptance criteria defined
   - User approves tasks
5. **Implementation (`/sp.implement`)**: Execute tasks following TDD
   - Red: Write failing tests
   - Green: Implement minimum code to pass
   - Refactor: Improve code quality
   - Repeat for each task
6. **Commit & PR (`/sp.git.commit_pr`)**: Version control workflow
   - Agent creates commit with descriptive message
   - Agent generates PR with summary and test plan
7. **PHR Creation (automatic)**: Prompt History Record generated for traceability

### Quality gates:

- **Spec gate**: No planning without approved spec
- **Plan gate**: No task generation without approved plan
- **Task gate**: No implementation without approved tasks
- **Test gate**: No code without passing tests
- **Review gate**: All code reviewed (manual or automated)

### ADR (Architecture Decision Record) policy:

- Suggested automatically when significant decisions detected during planning/tasks
- Format: `📋 Architectural decision detected: <brief> — Document? Run /sp.adr <title>`
- Requires user consent; never auto-created
- Stored in `history/adr/`

## Governance

**This constitution supersedes all other practices, conventions, and preferences.**

### Amendment process:

1. Proposed changes documented with rationale
2. Impact analysis on existing specs, plans, and code
3. Version bump determined (MAJOR/MINOR/PATCH per semantic versioning)
4. User approval required
5. Constitution updated at `.specify/memory/constitution.md`
6. Dependent templates updated for consistency
7. Sync Impact Report generated and embedded in constitution
8. Migration plan created if breaking changes exist

### Versioning policy:

- **MAJOR (X.0.0)**: Backward incompatible governance changes, principle removals, or redefinitions
- **MINOR (x.Y.0)**: New principles/sections added, material expansions
- **PATCH (x.y.Z)**: Clarifications, wording improvements, non-semantic refinements

### Compliance:

- All agent actions must be constitution-compliant
- All PRs must verify adherence to principles
- Violations trigger immediate stop and correction at spec level
- Regular audits ensure alignment across phases

### Living document:

- Constitution evolves as project learns and scales
- Each phase may reveal needs for refinement
- Amendments are encouraged when justified
- History preserved through version control

### Complexity justification:

- Every architectural decision requires documented rationale
- Trade-offs explicitly stated in ADRs
- Simplicity preferred; complexity requires strong justification
- YAGNI (You Aren't Gonna Need It) principle guides design

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
