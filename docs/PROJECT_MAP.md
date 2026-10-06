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

Python dependency list. Phase 3 uses `paho-mqtt==2.1.0` to connect the simulator
to an MQTT broker.

### .env.example

Reference values for local environment variables. Phase 3 reads MQTT settings
from the operating-system environment and does not load this file automatically.

### .gitignore

Git ignore rules for virtual environments, local configuration, Mosquitto
password files, caches, build artifacts, and operating-system files.

## Directories

### .github/

GitHub repository configuration. It currently contains an empty pull-request
template at `.github/pull_request_template.md`.

### backend/

Python backend package. It currently contains only `backend/__init__.py`.

### simulator/

Virtual IoT device simulator package.

- `simulator/__init__.py` — package marker
- `simulator/main.py` — validates MQTT address and credential settings, creates
  10 virtual devices, publishes and prints one telemetry JSON object per device,
  then waits 2 seconds before the next cycle
- `simulator/mqtt_publisher.py` — applies optional MQTT credentials, connects to
  the broker, and publishes each device's telemetry as JSON with QoS 1
- `simulator/device.py` — virtual device that collects values from its sensors
- `simulator/telemetry.py` — telemetry data structure and UTC timestamp creation
- `simulator/sensors/__init__.py` — sensor package marker
- `simulator/sensors/base.py` — shared base for all virtual sensors
- `simulator/sensors/temperature.py` — virtual temperature sensor
- `simulator/sensors/humidity.py` — virtual humidity sensor

### frontend/

Reserved for the HTML, CSS, and JavaScript dashboard. It currently contains empty
`frontend/css/` and `frontend/js/` placeholder directories.

### scripts/

Reserved for development and maintenance scripts. It is currently empty.

### tests/

Automated tests for the simulator and MQTT publisher. Test files use the
`test_*.py` naming convention.

- `test_temperature_sensor.py` — checks temperature range, name, unit, and rounding
- `test_humidity_sensor.py` — checks humidity range, name, unit, and rounding
- `test_device.py` — checks device ID and collected telemetry
- `test_telemetry.py` — checks stored values and UTC timestamp
- `test_mqtt_publisher.py` — checks MQTT credentials, connect, publish, and
  disconnect calls plus the five-second publish timeout without requiring a
  real broker
- `test_main.py` — checks address and credential settings, startup connection
  failures, and retry behavior after a publish timeout

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
