# PDF Scanner with OCR

A professional, fully functional PDF Scanner with OCR (Optical Character Recognition) capabilities. This application features an attractive, modern UI built with HTML, CSS, and JavaScript, powered by a robust Python backend using Flask and Tesseract OCR.

## ✨ Features

- 📄 **PDF Processing**: Convert PDF documents to text with OCR
- 🖼️ **Image OCR**: Extract text from images (PNG, JPG, JPEG, BMP, TIFF)
- 🔄 **Batch Processing**: Process multiple files at once
- 🎨 **Image Enhancement**: Automatic image preprocessing for better accuracy
- 📥 **Multiple Export Formats**: Download results as TXT, PDF, or JSON
- 🎯 **High Accuracy**: Advanced OCR with image preprocessing
- 🌙 **Modern UI**: Professional dark theme with smooth animations
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- ⚡ **Fast Processing**: Optimized for quick text extraction

## 🚀 Technologies Used

### Frontend
- HTML5
- CSS3 (Modern styling with animations)
- Vanilla JavaScript
- Font Awesome Icons

### Backend
- Python 3.8+
- Flask (Web framework)
- Tesseract OCR (Text recognition)
- OpenCV (Image processing)
- Pillow (Image manipulation)
- ReportLab (PDF generation)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)

2. **Tesseract OCR**
   - **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
     - Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

3. **Poppler** (for PDF processing)
   - **Windows**: Download from [GitHub](https://github.com/oschwartz10612/poppler-windows/releases/)
     - Extract and add to PATH
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

## 🛠️ Installation

1. **Clone or download this repository**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Tesseract path (Windows only)**
   
   If Tesseract is not in your PATH, open `app.py` and uncomment/modify this line:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## 🎮 Usage

1. **Start the backend server**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

2. **Open the frontend**
   
   Open `index.html` in your web browser, or use a local server:
   ```bash
   # Using Python's built-in server
   python -m http.server 8000
   ```
   
   Then navigate to `http://localhost:8000`

3. **Use the application**
   - Drag and drop files or click to browse
   - Select PDF or image files
   - Toggle "Enhance image quality" for better results
   - Choose output format (Text, PDF, or JSON)
   - Click "Process Documents"
   - View and download extracted text

## 📁 Project Structure

```
PDF-Scanner-OCR/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── index.html            # Main HTML file
├── style.css             # Styling and animations
├── script.js             # Frontend JavaScript logic
├── README.md             # This file
├── uploads/              # Temporary upload folder (created automatically)
└── outputs/              # Generated files folder (created automatically)
```

## 🔧 Configuration

### Backend Configuration (`app.py`)

```python
# Maximum file size (default: 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Server settings
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Frontend Configuration (`script.js`)

```javascript
// API Base URL
const API_BASE_URL = 'http://localhost:5000';

// Supported file types
const validExtensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'];
```

## 📡 API Endpoints

### GET `/health`
Check server and OCR engine status

### POST `/upload`
Upload single file for OCR processing

**Form Data:**
- `file`: File to process
- `enhance`: Boolean (true/false) - Enable image enhancement
- `output_format`: String (text/pdf/json) - Output format

**Response:**
```json
{
  "success": true,
  "text": "Extracted text content...",
  "pages": 1,
  "char_count": 1234,
  "word_count": 200,
  "download_url": "/download/filename.pdf"
}
```

### POST `/batch-upload`
Upload multiple files for batch processing

**Form Data:**
- `files`: Multiple files
- `enhance`: Boolean - Enable image enhancement

### GET `/download/<filename>`
Download generated PDF file

## 🎨 Features Explained

### Image Enhancement
The application automatically preprocesses images for better OCR results:
- Grayscale conversion
- Noise reduction
- Threshold optimization
- Contrast enhancement

### Batch Processing
Process multiple documents at once:
- Upload multiple files simultaneously
- View individual results for each file
- Combined text output
- Progress tracking

### Export Options
- **Text**: Copy to clipboard or download as .txt
- **PDF**: Download formatted PDF with extracted text
- **JSON**: Get structured data with metadata

## 🐛 Troubleshooting

### Tesseract Not Found Error
- Ensure Tesseract is installed and in your PATH
- On Windows, set the path in `app.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### PDF Conversion Error
- Install Poppler and ensure it's in your PATH
- On Windows, add Poppler's bin directory to system PATH

### CORS Issues
- Ensure Flask-CORS is installed
- Backend must be running on the correct port

### Poor OCR Accuracy
- Enable "Enhance image quality" option
- Use higher resolution images (300 DPI recommended)
- Ensure text is clear and readable
- Try different preprocessing settings

## 🔒 Security Notes

- Files are temporarily stored and deleted after processing
- Maximum file size limit prevents abuse
- CORS is configured for development (adjust for production)
- Add authentication for production deployment

## 🚀 Production Deployment

For production use:

1. **Disable Flask debug mode**
   ```python
   app.run(debug=False)
   ```

2. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

3. **Configure CORS properly**
   ```python
   CORS(app, origins=['https://yourdomain.com'])
   ```

4. **Add HTTPS**
   - Use reverse proxy (nginx/Apache)
   - Configure SSL certificates

5. **Add authentication**
   - Implement user authentication
   - Add API key protection

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Support

If you encounter any issues or have questions, please check the troubleshooting section above.

## 🎉 Acknowledgments

- Tesseract OCR by Google
- Flask framework
- OpenCV library
- Font Awesome for icons

---

**Made with ❤️ using Python & OCR Technology**
