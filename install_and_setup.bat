@echo off
echo ============================================
echo Installing LLMOps Project Dependencies
echo ============================================
echo.

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    exit /b 1
)

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run the server: python main.py
echo 3. Open browser: http://localhost:8000
echo.
pause
