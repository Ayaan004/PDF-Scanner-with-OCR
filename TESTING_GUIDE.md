# Testing Guide - PDF Scanner with OCR

This guide will help you test all features of the PDF Scanner application.

## 🧪 Pre-Testing Checklist

Before you start testing, verify your setup:

```bash
python check_setup.py
```

All checks should pass before proceeding.

## 🚀 Starting the Application

1. **Start the Backend Server**
   ```bash
   run.bat
   # Or manually:
   python app.py
   ```

   You should see:
   ```
   ====================================
   PDF Scanner with OCR - Starting Server
   ====================================
   Server running on: http://localhost:5000
   ```

2. **Open the Frontend**
   - Double-click `index.html`, or
   - Use a local server: `python -m http.server 8000`

## 📝 Test Cases

### Test 1: Server Health Check

**Purpose**: Verify backend is running correctly

**Steps**:
1. Open browser console (F12)
2. Open the application
3. Check console for: `✅ Server is healthy and ready`

**Expected Result**: Green checkmark with success message

**Troubleshooting**:
- If error appears, check if Flask server is running
- Verify port 5000 is not blocked

---

### Test 2: Single Image Upload (Basic)

**Purpose**: Test single image OCR

**Required**: Sample image with text (create a screenshot with text, or use a photo of a document)

**Steps**:
1. Click the upload area
2. Select an image file (PNG/JPG)
3. Verify file appears in the file list
4. Keep "Enhance image quality" checked
5. Click "Process Documents"

**Expected Results**:
- Progress bar animates from 0% to 100%
- Results section appears
- Statistics show correct counts
- Extracted text is visible and readable
- Copy and download buttons work

**Success Criteria**:
- Text extraction accuracy > 90% for clear images
- Processing time < 5 seconds
- No errors in console

---

### Test 3: PDF Document Processing

**Purpose**: Test PDF to text conversion

**Required**: Any PDF document with text

**Steps**:
1. Drag and drop a PDF file
2. Select output format: "Text Only"
3. Enable enhancement
4. Click "Process Documents"

**Expected Results**:
- All pages are processed
- Page count is accurate
- Each page text is extractable
- Page accordion displays individual pages
- Full text combines all pages

**Success Criteria**:
- All pages extracted successfully
- Page numbers are correct
- Text quality is good

---

### Test 4: Batch Processing

**Purpose**: Test multiple file processing

**Required**: 3-5 different image/PDF files

**Steps**:
1. Upload multiple files at once (mix of images and PDFs)
2. Verify all files appear in list
3. Click "Process Documents"

**Expected Results**:
- All files process successfully
- Combined text output
- Individual results per file
- Statistics aggregate correctly

**Success Criteria**:
- All files processed without errors
- Total char/word counts are accurate
- Processing completes in reasonable time

---

### Test 5: File Removal

**Purpose**: Test file management

**Steps**:
1. Upload 3 files
2. Click the X button on the second file
3. Verify file is removed from list
4. Process remaining files

**Expected Results**:
- File removed from display
- Only remaining files are processed
- No errors occur

---

### Test 6: Image Enhancement Toggle

**Purpose**: Compare results with/without enhancement

**Required**: Lower quality image

**Steps**:
1. Upload a low-quality or scanned image
2. **First test**: Disable "Enhance image quality"
   - Process and note results
3. **Second test**: Enable enhancement
   - Upload same image
   - Process and note results

**Expected Results**:
- Enhanced version has better accuracy
- Text is clearer and more complete
- Fewer OCR errors

---

### Test 7: Output Format - Text

**Purpose**: Test text export

**Steps**:
1. Upload and process a document
2. Select output format: "Text Only"
3. Click copy button
4. Paste into notepad
5. Click download button

**Expected Results**:
- Text copies to clipboard correctly
- Download produces .txt file
- Content matches displayed text
- Formatting is preserved

---

### Test 8: Output Format - PDF

**Purpose**: Test PDF generation

**Steps**:
1. Upload and process a document
2. Select output format: "Downloadable PDF"
3. Process the document
4. Click the PDF download button

**Expected Results**:
- PDF download link appears
- File downloads successfully
- PDF opens correctly
- Text is readable and formatted
- All pages are included

---

### Test 9: Large File Handling

**Purpose**: Test file size limits

**Steps**:
1. Try uploading a file > 16MB
2. Try uploading multiple large files

**Expected Results**:
- Appropriate error message for oversized files
- Application doesn't crash
- Other features still work

---

### Test 10: Invalid File Types

**Purpose**: Test file validation

**Steps**:
1. Try uploading a .docx file
2. Try uploading a .txt file
3. Try uploading a video file

**Expected Results**:
- Toast notification shows error
- Invalid files are rejected
- Application remains stable
- Only valid files are added

---

### Test 11: Empty/No Text Documents

**Purpose**: Test edge case handling

**Steps**:
1. Upload an image with no text (blank page or photo)
2. Process the file

**Expected Results**:
- Process completes without error
- Warning message: "No text extracted"
- Empty result with 0 words/characters
- No application crash

---

### Test 12: Special Characters

**Purpose**: Test character encoding

**Required**: Document with special characters (©, ®, €, etc.)

**Steps**:
1. Upload document with special characters
2. Process the file
3. Check extracted text

**Expected Results**:
- Special characters are preserved
- No encoding errors
- Unicode characters display correctly

---

### Test 13: Multi-Language (if applicable)

**Purpose**: Test non-English text

**Required**: Document in another language

**Steps**:
1. Upload document with foreign language text
2. Process the file

**Expected Results**:
- Text is extracted (may vary by language)
- No crashes or errors
- UTF-8 encoding preserved

---

### Test 14: Mobile Responsiveness

**Purpose**: Test on different screen sizes

**Steps**:
1. Open browser developer tools (F12)
2. Toggle device toolbar
3. Test on mobile view (375px width)
4. Test on tablet view (768px width)

**Expected Results**:
- Layout adjusts appropriately
- All buttons are accessible
- Text is readable
- Features work correctly

---

### Test 15: Progress Tracking

**Purpose**: Verify progress feedback

**Steps**:
1. Upload a large PDF (10+ pages)
2. Start processing
3. Watch progress bar

**Expected Results**:
- Progress bar animates smoothly
- Percentage updates regularly
- Completes at 100%
- No freezing or hanging

---

### Test 16: Error Recovery

**Purpose**: Test error handling

**Steps**:
1. Stop the Flask server
2. Try to process a file
3. Restart the server
4. Try again

**Expected Results**:
- Appropriate error message shown
- Application doesn't break
- Works again after server restart

---

### Test 17: New Scan Button

**Purpose**: Test reset functionality

**Steps**:
1. Complete a full scan
2. View results
3. Click "New Scan" button

**Expected Results**:
- Results section hidden
- File list cleared
- Upload section visible
- Ready for new upload

---

### Test 18: Page Accordion

**Purpose**: Test multi-page document navigation

**Required**: PDF with 3+ pages

**Steps**:
1. Upload and process multi-page PDF
2. Click on different page headers in accordion

**Expected Results**:
- Pages expand/collapse on click
- Individual page text displays correctly
- Smooth animations
- All pages accessible

---

### Test 19: Concurrent Processing

**Purpose**: Test handling of rapid requests

**Steps**:
1. Upload file and start processing
2. Quickly open another browser tab
3. Upload and process a different file

**Expected Results**:
- Both requests complete successfully
- No conflicts or errors
- Results display correctly in each tab

---

### Test 20: Performance Benchmark

**Purpose**: Measure processing speed

**Test Files**:
- Small image (< 1MB)
- Medium PDF (5 pages, ~2MB)
- Large PDF (20+ pages, ~10MB)

**Measure**:
- Upload to results time
- Extract timing from console (if logged)

**Expected Performance**:
- Small image: < 3 seconds
- Medium PDF: < 15 seconds
- Large PDF: < 60 seconds

---

## 🐛 Common Issues During Testing

### Issue: "Tesseract not found"
**Solution**: 
```python
# Edit app.py, uncomment and set:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Issue: Poor OCR quality
**Solutions**:
- Use higher resolution images (300 DPI)
- Enable image enhancement
- Ensure good contrast in source document
- Avoid blurry or skewed images

### Issue: CORS errors
**Solution**:
```bash
# Serve frontend with Python
python -m http.server 8000
# Then navigate to http://localhost:8000
```

### Issue: PDF processing fails
**Solution**:
- Verify Poppler is installed
- Check PATH includes Poppler's bin directory
- Restart terminal after PATH changes

---

## ✅ Testing Checklist

Use this checklist to track your testing progress:

- [ ] Test 1: Server Health Check
- [ ] Test 2: Single Image Upload
- [ ] Test 3: PDF Document Processing
- [ ] Test 4: Batch Processing
- [ ] Test 5: File Removal
- [ ] Test 6: Image Enhancement
- [ ] Test 7: Text Output
- [ ] Test 8: PDF Output
- [ ] Test 9: Large File Handling
- [ ] Test 10: Invalid File Types
- [ ] Test 11: Empty Documents
- [ ] Test 12: Special Characters
- [ ] Test 13: Multi-Language
- [ ] Test 14: Mobile Responsiveness
- [ ] Test 15: Progress Tracking
- [ ] Test 16: Error Recovery
- [ ] Test 17: New Scan Button
- [ ] Test 18: Page Accordion
- [ ] Test 19: Concurrent Processing
- [ ] Test 20: Performance Benchmark

---

## 📊 Testing Report Template

After testing, document your results:

```
Testing Date: __________
Tester: __________
Environment: Windows/Mac/Linux

PASSED: __ / 20
FAILED: __ / 20

Issues Found:
1. ___________________
2. ___________________

Notes:
_____________________
_____________________
```

---

## 🎯 Success Criteria

The application passes testing if:

- ✅ All 20 tests complete without critical errors
- ✅ OCR accuracy > 90% for clear documents
- ✅ No data loss or corruption
- ✅ UI is responsive and intuitive
- ✅ Error messages are clear and helpful
- ✅ Performance meets benchmarks

---

## 🚀 Ready for Production

Once all tests pass:

1. Document any known limitations
2. Create user guide for end-users
3. Set up production environment
4. Consider security hardening
5. Add monitoring and logging

---

**Happy Testing! 🎉**
