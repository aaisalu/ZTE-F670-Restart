@echo off

REM  script will execute in the directory where it is located.
cd /d %~dp0
echo Directery changed to %cd%

echo Seting up the virtual environment....
if not exist venv (
    python -m venv venv
)

echo Activating the virtual environment
call venv\Scripts\activate.bat

echo Installing required packages
pip install -r requirements.txt

rem Run the script
python restart.py

echo Deactivating the virtual environment....
call venv\Scripts\deactivate.bat

REM Close the command prompt
exit
