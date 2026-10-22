@echo off
echo ========================================
echo PDF Scanner with OCR - Starting Server
echo ========================================
echo.

if not exist venv\ (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Flask server...
echo.
echo Server will start on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
