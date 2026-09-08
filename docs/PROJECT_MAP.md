# Project Map

This map describes the files and directories currently present in the repository.
Future responsibilities are documented in `ARCHITECTURE.md` and are not treated as
implemented components.

## Root Files

### AGENTS.md

Instructions for AI coding agents working in this repository.

### README.md

Human-readable project introduction, roadmap, and overview.

### requirements.txt

Python dependency list. It is currently empty for Phase 1.

### .env.example

Example local environment variables. Copy it to `.env` for local configuration.

### .gitignore

Git ignore rules for virtual environments, local configuration, caches, build
artifacts, and operating-system files.

### command_cmd_note

Legacy Thai-language notes for commonly used Windows CMD commands.

## Directories

### .github/

GitHub repository configuration. It currently contains an empty pull-request
template at `.github/pull_request_template.md`.

### backend/

Python backend package. It currently contains only `backend/__init__.py`.

### simulator/

Virtual IoT device simulator package.

- `simulator/__init__.py` — package marker
- `simulator/main.py` — current simulator entry point and Phase 1 smoke check

### frontend/

Reserved for the HTML, CSS, and JavaScript dashboard. It is currently empty.

### scripts/

Reserved for development and maintenance scripts. It is currently empty.

### tests/

Reserved for automated tests. It is currently empty; future test files should use
the `test_*.py` naming convention.

### docs/

Project documentation.

- `ARCHITECTURE.md` — target architecture and phase plan
- `COMMANDS.md` — Windows CMD command reference
- `DEVELOPMENT.md` — setup, run, and verification instructions
- `PROJECT_MAP.md` — this codebase navigation map

## Local and Git Metadata

The `.git/` and `.venv/` directories exist locally but are intentionally omitted
from the source map: `.git/` is repository metadata and `.venv/` is a local Python
environment that must not be committed.
