@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

REM Resolve Python executable: prefer active virtual environment, then local .venv, then system python
if defined VIRTUAL_ENV (
    set "PYTHON_EXE=python"
) else if exist "%SCRIPT_DIR%..\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
) else if exist "%SCRIPT_DIR%..\..\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%SCRIPT_DIR%..\..\.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" "%SCRIPT_DIR%tren" %*
exit /b %ERRORLEVEL%
