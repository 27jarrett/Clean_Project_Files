@echo off
REM This batch file is used to launch the Python GUI application.
REM Ensure Python is installed and added to your system's PATH.

REM Change directory to the script's location
pushd "%~dp0"

REM Activate a virtual environment if you are using one
REM For example: .\venv\Scripts\activate.bat
REM If not using a venv, remove or comment out the above line.

REM Run the main Python application script
python main.py

REM Deactivate the virtual environment if activated
REM For example: deactivate
REM If not using a venv, remove or comment out the above line.

REM Keep the console window open after execution (optional)
REM pause

popd
