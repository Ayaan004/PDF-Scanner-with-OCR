# Installation Guide - PDF Scanner with OCR

This guide will help you set up the PDF Scanner with OCR application on Windows.

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Windows 10 or later
- [ ] Internet connection
- [ ] Administrator privileges (for software installation)

## 🔧 Step-by-Step Installation

### Step 1: Install Python

1. Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install Tesseract OCR

1. Download Tesseract installer from:
   [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Download the latest `.exe` file (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

3. Run the installer:
   - Accept the license
   - Use default installation path: `C:\Program Files\Tesseract-OCR`
   - Select "Additional language data" if you need languages other than English
   - Complete installation

4. **Add Tesseract to PATH** (if not already):
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\Tesseract-OCR`
   - Click OK on all dialogs

5. Verify installation:
   ```bash
   tesseract --version
   ```

### Step 3: Install Poppler (for PDF processing)

1. Download Poppler for Windows:
   [https://github.com/oschwartz10612/poppler-windows/releases/](https://github.com/oschwartz10612/poppler-windows/releases/)

2. Download the latest release (e.g., `Release-24.02.0-0.zip`)

3. Extract the ZIP file to a location like:
   `C:\Program Files\poppler`

4. **Add Poppler to PATH**:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\poppler\Library\bin`
   - Click OK on all dialogs

5. Verify installation:
   ```bash
   pdftoppm -v
   ```

### Step 4: Setup the Application

1. Open Command Prompt or PowerShell

2. Navigate to the project directory:
   ```bash
   cd "C:\Users\ayaan\Desktop\development\PRACTICE\PDF Scanner with OCR"
   ```

3. Run the setup script:
   ```bash
   setup.bat
   ```

   This will:
   - Create a virtual environment
   - Install all Python dependencies
   - Set up the project structure

### Step 5: Configure Tesseract Path (if needed)

If Tesseract was installed to a non-default location:

1. Open `app.py` in a text editor

2. Find and uncomment this line (around line 18):
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

3. Update the path if your installation location is different

4. Save the file

## 🚀 Running the Application

### Method 1: Using the Run Script (Easiest)

1. Double-click `run.bat`
2. The server will start automatically
3. Open your browser and navigate to the `index.html` file

### Method 2: Manual Start

1. Open Command Prompt or PowerShell

2. Navigate to project directory:
   ```bash
   cd "C:\Users\ayaan\Desktop\development\PRACTICE\PDF Scanner with OCR"
   ```

3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```

4. Start the server:
   ```bash
   python app.py
   ```

5. Open `index.html` in your web browser

### Method 3: Using a Local Web Server

For better CORS handling, you can serve the frontend with Python:

1. Open a second terminal

2. Navigate to project directory

3. Run:
   ```bash
   python -m http.server 8000
   ```

4. Open browser to: `http://localhost:8000`

## ✅ Verification

To verify everything is working:

1. Server should show:
   ```
   PDF Scanner with OCR - Starting Server
   Server running on: http://localhost:5000
   ```

2. Open browser console (F12) - should show:
   ```
   ✅ Server is healthy and ready
   ```

3. Try uploading a test image or PDF

## 🐛 Common Issues & Solutions

### Issue: "Python not found"
**Solution**: Reinstall Python and ensure "Add to PATH" is checked

### Issue: "Tesseract not found" error
**Solution**: 
- Verify Tesseract is installed
- Check PATH settings
- Set the path manually in `app.py`

### Issue: "Poppler not found" error when processing PDFs
**Solution**:
- Verify Poppler is installed
- Check PATH includes Poppler's bin directory
- Restart terminal/computer after PATH changes

### Issue: "Module not found" error
**Solution**:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then update `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001';
```

### Issue: CORS errors in browser
**Solution**: 
- Ensure Flask server is running
- Use `python -m http.server` to serve the frontend
- Check browser console for specific CORS messages

### Issue: Poor OCR accuracy
**Solution**:
- Enable "Enhance image quality" option
- Use higher resolution images (300 DPI recommended)
- Ensure images are clear and text is readable
- Try different image formats

## 📚 Additional Resources

- [Python Documentation](https://docs.python.org/)
- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🆘 Getting Help

If you encounter issues:

1. Check the error message carefully
2. Review the troubleshooting section in README.md
3. Check that all prerequisites are installed
4. Verify PATH settings
5. Try restarting your computer after installation

## 🎉 Success!

Once everything is running:
- The backend server runs on `http://localhost:5000`
- Open `index.html` in your browser
- Upload PDFs or images
- Extract text with OCR
- Download results

Enjoy your PDF Scanner with OCR! 🚀
