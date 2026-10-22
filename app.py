from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import io
import tempfile
import cv2
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import base64

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Tesseract configuration (adjust path if needed)
# Uncomment the line below after installing Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# For Linux/Mac: usually auto-detected

def preprocess_image(image):
    """Enhance image for better OCR results"""
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to get a binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
    
    # Convert back to PIL Image
    return Image.fromarray(denoised)

def perform_ocr(image, enhance=True):
    """Perform OCR on an image"""
    try:
        if enhance:
            image = preprocess_image(image)
        
        # Perform OCR with custom config for better results
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR failed: {str(e)}")

def create_pdf_from_text(text, output_path):
    """Create a PDF file from extracted text"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom style for better formatting
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6
    )
    
    story = []
    
    # Split text into paragraphs
    paragraphs = text.split('\n')
    
    for para in paragraphs:
        if para.strip():
            p = Paragraph(para, custom_style)
            story.append(p)
        else:
            story.append(Spacer(1, 0.1 * inch))
    
    doc.build(story)

@app.route('/')
def index():
    return jsonify({
        "message": "PDF Scanner with OCR API",
        "version": "1.0.0",
        "endpoints": {
            "/upload": "POST - Upload image or PDF for OCR",
            "/health": "GET - Check API health"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Test if Tesseract is available
        pytesseract.get_tesseract_version()
        return jsonify({"status": "healthy", "tesseract": "available"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and OCR processing"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        enhance = request.form.get('enhance', 'true').lower() == 'true'
        output_format = request.form.get('output_format', 'text')  # text, pdf, json
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in ['.png', '.jpg', '.jpeg', '.pdf', '.bmp', '.tiff']:
            return jsonify({"error": "Invalid file type. Supported: PNG, JPG, PDF, BMP, TIFF"}), 400
        
        # Save uploaded file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)
        
        extracted_text = ""
        pages_data = []
        
        try:
            if file_ext == '.pdf':
                # Convert PDF to images
                with tempfile.TemporaryDirectory() as path:
                    images = convert_from_path(temp_path, dpi=300)
                    
                    for i, image in enumerate(images):
                        page_text = perform_ocr(image, enhance)
                        extracted_text += f"\n--- Page {i + 1} ---\n{page_text}\n"
                        pages_data.append({
                            "page": i + 1,
                            "text": page_text,
                            "char_count": len(page_text)
                        })
            else:
                # Process single image
                image = Image.open(temp_path)
                extracted_text = perform_ocr(image, enhance)
                pages_data.append({
                    "page": 1,
                    "text": extracted_text,
                    "char_count": len(extracted_text)
                })
            
            # Clean up uploaded file
            os.remove(temp_path)
            
            if not extracted_text.strip():
                return jsonify({
                    "warning": "No text extracted from the document",
                    "text": "",
                    "pages": 0
                }), 200
            
            response_data = {
                "success": True,
                "text": extracted_text.strip(),
                "pages": len(pages_data),
                "pages_data": pages_data,
                "char_count": len(extracted_text.strip()),
                "word_count": len(extracted_text.strip().split())
            }
            
            # Handle different output formats
            if output_format == 'pdf':
                output_filename = f"ocr_output_{os.urandom(8).hex()}.pdf"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                create_pdf_from_text(extracted_text.strip(), output_path)
                response_data['download_url'] = f"/download/{output_filename}"
            
            return jsonify(response_data), 200
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated PDF file"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    """Handle multiple file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        files = request.files.getlist('files')
        enhance = request.form.get('enhance', 'true').lower() == 'true'
        
        results = []
        
        for file in files:
            if file.filename == '':
                continue
            
            file_ext = os.path.splitext(file.filename)[1].lower()
            
            if file_ext not in ['.png', '.jpg', '.jpeg', '.pdf', '.bmp', '.tiff']:
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Invalid file type"
                })
                continue
            
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            try:
                if file_ext == '.pdf':
                    with tempfile.TemporaryDirectory() as path:
                        images = convert_from_path(temp_path, dpi=300)
                        extracted_text = ""
                        
                        for image in images:
                            page_text = perform_ocr(image, enhance)
                            extracted_text += f"{page_text}\n"
                else:
                    image = Image.open(temp_path)
                    extracted_text = perform_ocr(image, enhance)
                
                os.remove(temp_path)
                
                results.append({
                    "filename": file.filename,
                    "success": True,
                    "text": extracted_text.strip(),
                    "char_count": len(extracted_text.strip()),
                    "word_count": len(extracted_text.strip().split())
                })
                
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": str(e)
                })
        
        return jsonify({
            "total_files": len(files),
            "processed": len(results),
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("PDF Scanner with OCR - Starting Server")
    print("=" * 60)
    print("Server running on: http://localhost:5000")
    print("Endpoints:")
    print("  - POST /upload (single file OCR)")
    print("  - POST /batch-upload (multiple files OCR)")
    print("  - GET /download/<filename> (download processed PDF)")
    print("  - GET /health (check server status)")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
