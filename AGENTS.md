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

Phase 3 - MQTT Communication

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

### Phase 3 — MQTT Communication

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python -m unittest discover -s tests -p "test_*.py"
```

The automated tests do not require a running MQTT broker because the MQTT
client is replaced with a mock during those tests. The unittest command should
report `Ran 24 tests` and `OK` when all current tests pass.

For a manual MQTT check, make sure Mosquitto is listening on `127.0.0.1:1883`.
Open a subscriber in one CMD window:

```cmd
"C:\Program Files\mosquitto\mosquitto_sub.exe" -h 127.0.0.1 -p 1883 -u "pyiot-simulator" -P "replace-with-your-password" -t "pyiot/devices/+/telemetry" -v
```

Run the simulator in another CMD window:

```cmd
set "MQTT_USERNAME=pyiot-simulator"
set "MQTT_PASSWORD=replace-with-your-password"
python simulator\main.py
```

Example subscriber output:

```text
pyiot/devices/ESP32-ROOM-001/telemetry {"device_id": "ESP32-ROOM-001", "temperature": 30.12, "humidity": 65.34, "timestamp": "2026-09-09T18:29:08.576066+00:00"}
```

The simulator publishes one JSON message for every device, from
ESP32-ROOM-001 through ESP32-ROOM-010, and also prints each message locally.
After all 10 devices publish, it waits 2 seconds before starting the next
cycle. If the broker becomes unavailable, publishing waits at most 5 seconds,
then the simulator waits 2 seconds and tries again while Paho reconnects in the
background. Stop the simulator and subscriber with `Ctrl+C`.

The simulator reads `MQTT_HOST`, `MQTT_PORT`, `MQTT_USERNAME`, and
`MQTT_PASSWORD` from operating-system environment variables. Host and port
default to `127.0.0.1` and `1883`. Username and password must be set together
when the broker requires authentication. The `.env.example` file documents the
values but is not loaded automatically. Never store real credentials in tracked
files.

Do not run or add checks for future-phase components until that phase is requested.


## Source of Truth

Project structure:
docs/PROJECT_MAP.md

System architecture:
docs/ARCHITECTURE.md

Development commands:
- docs/DEVELOPMENT.md
- docs/COMMANDS.md
