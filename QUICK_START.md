# Quick Start Guide 🚀

Get your PDF Scanner with OCR up and running in minutes!

## ⚡ Fast Setup (3 Steps)

### 1️⃣ Install Prerequisites

**Python** (if not installed):
- Download: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

**Tesseract OCR**:
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR`
- Default settings are fine

**Poppler** (for PDF files):
- Download: https://github.com/oschwartz10612/poppler-windows/releases/
- Extract to: `C:\Program Files\poppler`
- Add `C:\Program Files\poppler\Library\bin` to PATH

### 2️⃣ Setup the Application

Open PowerShell/Command Prompt in this folder and run:

```bash
setup.bat
```

This installs all Python dependencies automatically.

### 3️⃣ Start the Application

```bash
run.bat
```

Then open `index.html` in your browser!

## 🎯 Usage

1. **Upload Files**: Drag & drop or click to browse
2. **Configure**: 
   - Enable "Enhance image quality" for better results
   - Select output format (Text, PDF, or JSON)
3. **Process**: Click "Process Documents"
4. **Results**: View, copy, or download extracted text

## 📁 Supported File Types

- ✅ PDF documents
- ✅ PNG images
- ✅ JPG/JPEG images
- ✅ BMP images
- ✅ TIFF images

## 💡 Pro Tips

- Use high-resolution images (300 DPI) for best results
- Enable image enhancement for scanned documents
- Process multiple files at once with batch upload
- Clear, well-lit documents work best

## 🆘 Quick Troubleshooting

**Server won't start?**
- Make sure Python is installed: `python --version`
- Run `setup.bat` again

**"Tesseract not found" error?**
- Verify installation: `tesseract --version`
- Edit `app.py` and set the path manually (see line 18)

**PDF processing fails?**
- Install Poppler (see prerequisites)
- Verify: `pdftoppm -v`

**CORS errors in browser?**
- Make sure the Flask server is running
- Try: `python -m http.server 8000` for the frontend

## 📊 Example Workflow

```
1. Start server → run.bat
2. Open browser → index.html
3. Upload document → test.pdf
4. Process → Click button
5. Download → Save as TXT or PDF
```

## 🎨 Features at a Glance

- 🔍 Advanced OCR with Tesseract
- 📄 PDF to text conversion
- 🖼️ Image text extraction
- 🔄 Batch processing
- 📥 Multiple export formats
- 🎯 High accuracy
- ⚡ Fast processing
- 🌙 Beautiful dark UI

## 📞 Need Help?

Check the detailed guides:
- 📖 `README.md` - Full documentation
- 🔧 `INSTALLATION_GUIDE.md` - Detailed setup instructions

---

**That's it! You're ready to extract text from any document! 🎉**
