# Development Guide

## Environment

- Primary OS: Windows
- Primary terminal: CMD
- Primary editor: Visual Studio Code
- Python: 3.12 (the current `.venv` was created with Python 3.12)

Run all project commands from the repository root:

```cmd
cd /d "%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center"
```

## First-Time Setup

### 1. Create the virtual environment

Create `.venv` only when it does not already exist:

```cmd
py -3.12 -m venv .venv
```

### 2. Activate the virtual environment

```cmd
.venv\Scripts\activate
```

Confirm that the project environment is active:

```cmd
where python
python --version
```

The first `where python` result should point to `.venv\Scripts\python.exe`.

### 3. Install dependencies

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Phase 3 installs `paho-mqtt==2.1.0`, which the simulator uses to connect and
publish telemetry to an MQTT broker.

### 4. Create local environment settings

Create a local `.env` file from the example:

```cmd
copy .env.example .env
```

Edit `.env` only when the current phase needs its values. Never commit this file;
it is excluded by `.gitignore`.

## Open the Project

```cmd
code .
```

## Run the Current Phase

Phase 3 sends telemetry from the 10 virtual devices to Eclipse Mosquitto. Make
sure Mosquitto is running and listening on `127.0.0.1:1883`.

Open a subscriber in the first CMD window:

```cmd
"C:\Program Files\mosquitto\mosquitto_sub.exe" -h 127.0.0.1 -p 1883 -t "pyiot/devices/+/telemetry" -v
```

The `+` wildcard receives the telemetry topic for any one device ID.

Run the simulator in a second CMD window:

```cmd
python simulator\main.py
```

Example output:

```json
{
    "device_id": "ESP32-ROOM-001",
    "temperature": 30.12,
    "humidity": 65.34,
    "timestamp": "2026-09-09T18:29:08.576066+00:00"
}
```

The example above shows one of the 10 devices. Each cycle publishes the JSON to
`pyiot/devices/{device_id}/telemetry` and prints it locally for every device,
from ESP32-ROOM-001 through ESP32-ROOM-010. Temperature, humidity, and timestamp
values change each cycle. After all 10 devices publish, the simulator waits
2 seconds before starting the next cycle. Press `Ctrl+C` to stop the simulator
and close its MQTT connection. Stop the subscriber with `Ctrl+C` as well.

If the broker stops while the simulator is running, publishing waits at most
5 seconds. The simulator then waits 2 seconds before trying again while Paho
handles reconnection in the background. When the broker returns, telemetry
publishing resumes without restarting the simulator.

## Verify Changes

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python -m unittest discover -s tests -p "test_*.py"
```

The `tests/` directory contains automated tests for the virtual sensors, device,
telemetry, and MQTT publisher. The unittest command currently runs 16 tests and
should report `OK` when they all pass. MQTT tests use a mock client, so Mosquitto
does not need to be running for the automated tests. New test files should use
the `test_*.py` naming convention inside `tests/`.

## Daily Workflow

```cmd
cd /d "%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center"
.venv\Scripts\activate
python -m unittest discover -s tests -p "test_*.py"
python simulator\main.py
```

The simulator requires the local Mosquitto broker and keeps running until you
press `Ctrl+C`. Use a separate CMD window for the MQTT subscriber when manually
checking published messages.

Use `deactivate` when you finish working in the virtual environment.
