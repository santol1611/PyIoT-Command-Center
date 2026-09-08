# Development Guide

## Environment

- Primary OS: Windows
- Primary terminal: CMD
- Primary editor: Visual Studio Code
- Python: 3.12 (the current `.venv` was created with Python 3.12)

Run all project commands from the repository root:

```cmd
cd /d C:\Users\Santol\Desktop\Coding\PyIoT-Command-Center
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

`requirements.txt` is currently empty because the project is in Phase 1. Keep this
command in the setup flow so it remains valid when dependencies are added.

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

Phase 1 provides a foundation smoke check through the simulator entry point:

```cmd
python simulator\main.py
```

Expected output:

```text
PyIoT Command Center
Environment setup completed.
```

## Verify Changes

Run the applicable checks after changing Python code:

```cmd
python -m compileall backend simulator
python -m unittest discover -s tests -p "test_*.py"
```

There are no automated tests yet, so unittest may report `Ran 0 tests` and still
exit successfully. New tests should use the `test_*.py` naming convention inside
`tests/`.

## Daily Workflow

```cmd
cd /d C:\Users\Santol\Desktop\Coding\PyIoT-Command-Center
.venv\Scripts\activate
python simulator\main.py
python -m unittest discover -s tests -p "test_*.py"
```

Use `deactivate` when you finish working in the virtual environment.
