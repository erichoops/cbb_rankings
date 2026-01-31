@echo off
REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run your Python script
python build_site.py

REM Start a local server for testing
python -m http.server 8000
pause
