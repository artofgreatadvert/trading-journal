@echo off
echo.
echo ==========================================
echo   Trading Journal Build Script (Windows)
echo ==========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo Step 4: Installing dependencies...
pip install --only-binary=:all: -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Troubleshooting:
    echo 1. Make sure you have Python 3.10+ installed
    echo 2. Try running: pip install --upgrade pip setuptools wheel
    echo 3. If still failing, install Visual Studio Build Tools from:
    echo    https://visualstudio.microsoft.com/downloads/
    echo.
    pause
    exit /b 1
)

echo Step 5: Building executable...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   Build Complete!
echo ==========================================
echo.
echo Your executable is in: dist/Trading Journal.exe
echo.
pause
