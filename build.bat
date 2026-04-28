@echo off
echo.
echo ==========================================
echo   Trading Journal Build Script (Windows)
echo ==========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo Step 4: Building executable...
python build_exe.py

echo.
echo ==========================================
echo   Build Complete!
echo ==========================================
echo.
echo Your executable is in: dist/Trading Journal.exe
echo.
pause
