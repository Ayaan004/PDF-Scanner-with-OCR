@echo off
echo ========================================
echo PDF Scanner with OCR - Setup Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    echo Please ensure Python is installed and added to PATH
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo IMPORTANT: You need to install Tesseract OCR manually:
echo 1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install to default location: C:\Program Files\Tesseract-OCR
echo 3. Poppler (for PDF processing): https://github.com/oschwartz10612/poppler-windows/releases/
echo.
echo To start the application:
echo 1. Run: venv\Scripts\activate.bat
echo 2. Run: python app.py
echo 3. Open index.html in your browser
echo.
pause
