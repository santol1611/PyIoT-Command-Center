# PyIoT Command Center — Agent Instructions

## Project Goal

PyIoT Command Center is a Python-first IoT platform for:

- device monitoring
- sensor telemetry
- real-time dashboards
- device control
- automation rules
- ESP32 integration

The project is being developed incrementally by phases.

Current phase:

Phase 1 - Project Foundation

See:

- docs/PROJECT_MAP.md
- docs/ARCHITECTURE.md
- docs/DEVELOPMENT.md
- docs/COMMANDS.md


## Developer Environment

The primary development environment is:

- Windows
- CMD
- Visual Studio Code
- GitHub Desktop
- Python virtual environment: `.venv`

When giving terminal commands to the developer,
prefer Windows CMD syntax.

Do not assume Bash, zsh, or Linux commands unless required.


## Repository Structure

backend/
    Python backend application.

simulator/
    Virtual IoT devices and sensor simulators.

frontend/
    HTML, CSS, and JavaScript dashboard.

tests/
    Automated tests.

docs/
    Architecture and development documentation.

scripts/
    Development and maintenance scripts.


## Development Rules

- Prefer simple and readable Python.
- Avoid unnecessary abstractions.
- Keep modules focused on one responsibility.
- Do not add dependencies unless they are necessary.
- When adding a dependency, update requirements.txt.
- Never commit `.env`.
- Never commit `.venv`.
- Never hardcode passwords, API keys, or credentials.
- Preserve the existing project architecture unless there is a clear reason to change it.
- Avoid large unrelated refactors while implementing a feature.


## Before Modifying Code

Before making significant changes:

1. Read this AGENTS.md.
2. Read docs/PROJECT_MAP.md.
3. Read relevant architecture documentation.
4. Inspect the existing implementation before creating new modules.


## After Modifying Code

After code changes:

- run relevant tests when available
- verify imports
- check for obvious errors
- summarize files changed
- explain architectural changes if any


## Verification Commands

Use Windows CMD syntax. Activate `.venv` before running the commands below.

### Phase 1 — Project Foundation

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python simulator\main.py
python -m unittest discover -s tests -p "test_*.py"
```

Expected simulator output:

```text
PyIoT Command Center
Environment setup completed.
```

The `tests/` directory currently has no tests, so the unittest command may report
`Ran 0 tests`; retain this command as the project test convention as tests are added.

Do not run or add checks for future-phase components until that phase is requested.


## Source of Truth

Project structure:
docs/PROJECT_MAP.md

System architecture:
docs/ARCHITECTURE.md

Development commands:
- docs/DEVELOPMENT.md
- docs/COMMANDS.md
