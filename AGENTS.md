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

Phase 2 - Virtual Sensor Simulator

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

### Phase 2 — Virtual Sensor Simulator

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python simulator\main.py
python -m unittest discover -s tests -p "test_*.py"
```

Example simulator output:

```json
{
    "device_id": "ESP32-ROOM-001",
    "temperature": 30.12,
    "humidity": 65.34,
    "timestamp": "2026-09-09T18:29:08.576066+00:00"
}
```

The example above shows one of the 10 virtual devices. Each cycle prints a
JSON object for every device, from ESP32-ROOM-001 through ESP32-ROOM-010.
The temperature, humidity, and timestamp values change each cycle. After
all 10 devices print, the simulator waits 2 seconds before starting the
next cycle. Stop it with `Ctrl+C`.

The `tests/` directory contains automated tests for the virtual sensors,
device, and telemetry. The unittest command should report `Ran 10 tests`
and `OK` when all current tests pass.

Do not run or add checks for future-phase components until that phase is requested.


## Source of Truth

Project structure:
docs/PROJECT_MAP.md

System architecture:
docs/ARCHITECTURE.md

Development commands:
- docs/DEVELOPMENT.md
- docs/COMMANDS.md
