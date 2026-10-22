# Troubleshooting Guide - PDF Scanner with OCR

Quick solutions to common problems.

## 🚨 Installation Issues

### Python Not Found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, CHECK "Add Python to PATH"
3. Restart your terminal
4. Verify: `python --version`

---

### Tesseract Not Found

**Error**: `TesseractNotFoundError` or `tesseract is not installed`

**Solution**:

**Option 1: Add to PATH**
1. Find Tesseract installation (usually `C:\Program Files\Tesseract-OCR`)
2. Add to system PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit "Path" → Add Tesseract directory
   - Restart terminal

**Option 2: Set Path in Code**
1. Open `app.py`
2. Find line 18
3. Uncomment and set:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
4. Save and restart server

**Verify**: `tesseract --version`

---

### Poppler Not Found

**Error**: `Unable to get page count. Is poppler installed and in PATH?`

**Solution**:
1. Download from [GitHub](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to PATH
4. Restart terminal
5. Verify: `pdftoppm -v`

---

### pip Install Failed

**Error**: `ERROR: Could not install packages due to an OSError`

**Solutions**:

1. **Run as Administrator**
   ```bash
   # Right-click Command Prompt → Run as Administrator
   pip install -r requirements.txt
   ```

2. **Upgrade pip**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Use --user flag**
   ```bash
   pip install --user -r requirements.txt
   ```

---

## 🔧 Server Issues

### Port Already in Use

**Error**: `Address already in use` or `Port 5000 is already in use`

**Solution**:

**Option 1: Change Port**
1. Open `app.py`
2. Find last line: `app.run(debug=True, host='0.0.0.0', port=5000)`
3. Change to: `app.run(debug=True, host='0.0.0.0', port=5001)`
4. Open `script.js`
5. Change: `const API_BASE_URL = 'http://localhost:5001';`
6. Restart server

**Option 2: Kill Process**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Use the PID from the first command
```

---

### Server Won't Start

**Error**: Various import errors or crashes on startup

**Diagnostic Steps**:
1. Check Python version: `python --version` (need 3.8+)
2. Verify virtual environment: `venv\Scripts\activate`
3. Reinstall packages: `pip install -r requirements.txt`
4. Check for missing dependencies: `python check_setup.py`

**Solution**:
```bash
# Complete reinstall
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

### Server Crashes During Processing

**Error**: Server terminates unexpectedly during OCR

**Common Causes**:
- Memory issues with large files
- Corrupt PDF files
- Missing dependencies

**Solutions**:
1. Reduce file size
2. Check file integrity
3. Increase memory allocation:
   ```python
   # In app.py
   app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # Reduce to 8MB
   ```
4. Check server logs for specific error

---

## 🌐 Frontend Issues

### CORS Errors

**Error**: `Access to fetch has been blocked by CORS policy`

**Solution**:

**Option 1: Verify Flask-CORS**
```bash
pip install flask-cors
```

**Option 2: Serve Frontend with Python**
```bash
# In project directory
python -m http.server 8000
# Then navigate to http://localhost:8000
```

**Option 3: Check Backend is Running**
- Ensure Flask server is running on port 5000
- Open http://localhost:5000 - should show API info

---

### Upload Not Working

**Error**: Files don't upload or "No file provided" error

**Diagnostics**:
1. Check browser console (F12) for errors
2. Verify server is running
3. Check file size (< 16MB)
4. Verify file type is supported

**Solutions**:
- Clear browser cache
- Try different file
- Check server logs
- Verify FormData is being sent

---

### Page Not Loading

**Error**: Blank page or missing styles

**Solutions**:
1. Check all files are in same directory:
   - index.html
   - style.css
   - script.js

2. Open browser console for errors

3. Check file paths in `index.html`:
   ```html
   <link rel="stylesheet" href="style.css">
   <script src="script.js"></script>
   ```

4. Hard refresh: `Ctrl + Shift + R`

---

## 📄 OCR Issues

### No Text Extracted

**Error**: "No text extracted from the document"

**Causes & Solutions**:

1. **Image has no text**
   - Verify document actually contains text
   - Not a blank page

2. **Poor image quality**
   - Use higher resolution (300 DPI)
   - Enable "Enhance image quality"
   - Improve lighting/contrast

3. **Handwritten text**
   - Tesseract works best with printed text
   - Handwriting recognition is limited

4. **Language mismatch**
   - Install additional language data for Tesseract
   - Default is English only

---

### Low OCR Accuracy

**Error**: Extracted text has many errors

**Solutions**:

1. **Enable Enhancement**
   - Check "Enhance image quality" option

2. **Improve Source Quality**
   - Use 300 DPI or higher
   - Ensure good contrast
   - Avoid skewed or rotated images
   - Remove shadows and glare

3. **Preprocessing**
   - Crop unnecessary borders
   - Straighten document
   - Increase contrast

4. **File Format**
   - Use PNG or TIFF instead of JPG
   - Avoid compressed images

---

### Special Characters Garbled

**Error**: Symbols show as � or incorrect characters

**Solution**:
1. Verify UTF-8 encoding is used
2. Check if special characters are in Tesseract's language data
3. Install additional language packs if needed

---

## 💾 File Processing Issues

### PDF Processing Fails

**Error**: `Unable to process PDF` or poppler errors

**Solutions**:
1. Install Poppler (see installation section)
2. Verify PDF is not corrupted
3. Try with different PDF
4. Check PDF is not password-protected
5. Reduce PDF size/pages

---

### Large Files Timeout

**Error**: Request timeout or very slow processing

**Solutions**:

1. **Reduce File Size**
   - Split large PDFs
   - Reduce image resolution

2. **Increase Timeout**
   ```python
   # In app.py
   app.config['REQUEST_TIMEOUT'] = 300  # 5 minutes
   ```

3. **Process in Batches**
   - Upload fewer files at once
   - Process pages separately

---

### File Upload Rejected

**Error**: "Invalid file type" or upload fails

**Check**:
- File extension is: .pdf, .png, .jpg, .jpeg, .bmp, or .tiff
- File size is under 16MB
- File is not corrupted

**Solution**:
```bash
# Verify file
file yourfile.pdf  # Linux/Mac
# On Windows, check properties
```

---

## 🎨 UI/Display Issues

### Buttons Not Working

**Error**: Clicking buttons has no effect

**Solutions**:
1. Check browser console for JavaScript errors
2. Hard refresh: `Ctrl + Shift + R`
3. Clear browser cache
4. Try different browser
5. Verify `script.js` is loaded

---

### Styles Not Applied

**Error**: Page looks unstyled or broken

**Solutions**:
1. Verify `style.css` is in same directory
2. Check browser console for 404 errors
3. Hard refresh
4. Check link tag in HTML:
   ```html
   <link rel="stylesheet" href="style.css">
   ```

---

### Icons Missing

**Error**: Font Awesome icons don't show

**Solutions**:
1. Check internet connection (icons load from CDN)
2. Verify Font Awesome link in HTML:
   ```html
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
   ```
3. Try offline Font Awesome if needed

---

## 🔍 Debugging Tools

### Check Server Logs

```bash
# Server terminal shows detailed logs
# Look for error messages and stack traces
```

### Browser Console

```javascript
// Open with F12
// Check for:
// - JavaScript errors (red)
// - Network errors (Network tab)
// - API responses (Console tab)
```

### Test API Directly

```bash
# Test health endpoint
curl http://localhost:5000/health

# Should return:
# {"status":"healthy","tesseract":"available"}
```

### Verify File Paths

```bash
# List all files
dir  # Windows
ls   # Linux/Mac

# Should see:
# app.py, index.html, script.js, style.css, etc.
```

---

## 🔄 Complete Reset

If nothing works, try a complete reset:

```bash
# 1. Stop server (Ctrl+C)

# 2. Delete virtual environment
rmdir /s venv

# 3. Reinstall
setup.bat

# 4. Verify installation
python check_setup.py

# 5. Start fresh
run.bat
```

---

## 📞 Getting Help

Still stuck? Gather this information:

1. **Error Messages**
   - Exact error text
   - Screenshot if possible

2. **Environment**
   - OS version: `winver` (Windows)
   - Python version: `python --version`
   - Browser version

3. **What You Tried**
   - Steps taken
   - Solutions attempted

4. **Check Setup**
   ```bash
   python check_setup.py
   ```
   Share the output

---

## 📋 Quick Diagnostic Checklist

Run through this list:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Tesseract installed: `tesseract --version`
- [ ] Poppler installed: `pdftoppm -v`
- [ ] All Python packages: `python check_setup.py`
- [ ] Server running: http://localhost:5000/health
- [ ] No CORS errors in browser console
- [ ] File types are supported
- [ ] Files are under 16MB
- [ ] All project files present

---

## 🎯 Prevention Tips

Avoid future issues:

1. **Use Virtual Environment**
   - Always activate: `venv\Scripts\activate`

2. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check Prerequisites**
   - Run `check_setup.py` before starting

4. **Use Quality Input Files**
   - 300 DPI images
   - Clear, uncompressed PDFs

5. **Monitor Resources**
   - Close unused applications
   - Ensure adequate disk space

---

**Need More Help?**

- 📖 Check README.md for full documentation
- 🚀 Review QUICK_START.md for setup
- 🔧 See INSTALLATION_GUIDE.md for detailed install steps
- 🧪 Try TESTING_GUIDE.md to verify functionality

---

**Most issues are related to installation of Tesseract and Poppler. Double-check these first!** ✅
