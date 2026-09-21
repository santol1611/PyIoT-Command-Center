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

`requirements.txt` is currently empty because Phase 2 uses only Python's built-in
modules. Keep this command in the setup flow so it remains valid when dependencies
are added.

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

Phase 2 provides 10 virtual devices, each with temperature and humidity sensors.
Run them through the simulator entry point:

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

The example above shows one of the 10 devices. Each cycle prints a JSON object
for every device, from ESP32-ROOM-001 through ESP32-ROOM-010. Temperature,
humidity, and timestamp values change each cycle. After all 10 devices print,
the simulator waits 2 seconds before starting the next cycle. Press `Ctrl+C`
to stop it.

## Verify Changes

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python -m unittest discover -s tests -p "test_*.py"
```

The `tests/` directory now contains automated tests for the virtual sensors,
device, and telemetry. The unittest command currently runs 10 tests and should
report `OK` when they all pass. New test files should use the `test_*.py`
naming convention inside `tests/`.

## Daily Workflow

```cmd
cd /d "%USERPROFILE%\Desktop\Coding\PyIoT-Command-Center"
.venv\Scripts\activate
python simulator\main.py
python -m unittest discover -s tests -p "test_*.py"
```

The simulator keeps running, so stop it with `Ctrl+C` before running the unittest
command.

Use `deactivate` when you finish working in the virtual environment.
