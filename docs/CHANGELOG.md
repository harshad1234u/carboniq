# CarbonIQ – Changelog

## [0.1.1] – 2026-06-20

### Fixed
- Fixed critical bug in Onboarding flow causing infinite loading loops and duplicate `/profile` API requests.
- Migrated `useAuth` hook into a global `AuthContext` to ensure single-source-of-truth for authentication and profile state.
- Refined Dashboard profile lookups and eliminated redundancy.

## [0.1.0] – 2026-06-19

### Added
- Implementation plan (v1 → v2 → v3)
- Project memory system (docs/ directory)
  - PROJECT_CONTEXT.md
  - ARCHITECTURE.md
  - TASKS.md
  - DECISIONS.md
  - API_REFERENCE.md
  - CHANGELOG.md
- Architectural decisions documented (10 decisions)

### Planned
- Backend scaffolding and core services
- Frontend scaffolding with auth
- Full feature implementation
