// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const processBtn = document.getElementById('processBtn');
const enhanceCheckbox = document.getElementById('enhanceCheckbox');
const outputFormat = document.getElementById('outputFormat');

const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

const resultsSection = document.getElementById('resultsSection');
const pageCount = document.getElementById('pageCount');
const charCount = document.getElementById('charCount');
const wordCount = document.getElementById('wordCount');
const textContent = document.getElementById('textContent');
const pagesAccordion = document.getElementById('pagesAccordion');

const newScanBtn = document.getElementById('newScanBtn');
const copyBtn = document.getElementById('copyBtn');
const downloadTxtBtn = document.getElementById('downloadTxtBtn');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');

const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// State
let selectedFiles = [];
let extractedData = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkServerHealth();
    setupEventListeners();
});

// Check server health
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('✅ Server is healthy and ready');
        } else {
            showToast('Warning: OCR engine may not be available', 'warning');
        }
    } catch (error) {
        console.error('Server connection error:', error);
        showToast('Unable to connect to server. Please ensure the backend is running.', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(Array.from(e.target.files));
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        handleFiles(Array.from(e.dataTransfer.files));
    });

    // Process button
    processBtn.addEventListener('click', processDocuments);

    // Result actions
    newScanBtn.addEventListener('click', resetApp);
    copyBtn.addEventListener('click', copyToClipboard);
    downloadTxtBtn.addEventListener('click', downloadAsText);
    downloadPdfBtn.addEventListener('click', downloadAsPdf);

    // Output format change
    outputFormat.addEventListener('change', (e) => {
        if (e.target.value === 'pdf') {
            downloadPdfBtn.style.display = 'inline-flex';
        } else {
            downloadPdfBtn.style.display = 'none';
        }
    });
}

// Handle file selection
function handleFiles(files) {
    const validExtensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'];
    
    files.forEach(file => {
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        
        if (validExtensions.includes(ext)) {
            // Check if file already added
            if (!selectedFiles.some(f => f.name === file.name)) {
                selectedFiles.push(file);
            }
        } else {
            showToast(`Invalid file type: ${file.name}`, 'error');
        }
    });

    renderFileList();
    processBtn.disabled = selectedFiles.length === 0;
}

// Render file list
function renderFileList() {
    if (selectedFiles.length === 0) {
        fileList.innerHTML = '';
        return;
    }

    fileList.innerHTML = selectedFiles.map((file, index) => {
        const icon = file.type.includes('pdf') ? 'fa-file-pdf' : 'fa-file-image';
        const size = formatFileSize(file.size);
        
        return `
            <div class="file-item">
                <div class="file-info">
                    <i class="fas ${icon} file-icon"></i>
                    <div class="file-details">
                        <span class="file-name">${file.name}</span>
                        <span class="file-size">${size}</span>
                    </div>
                </div>
                <button class="file-remove" onclick="removeFile(${index})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    }).join('');
}

// Remove file
function removeFile(index) {
    selectedFiles.splice(index, 1);
    renderFileList();
    processBtn.disabled = selectedFiles.length === 0;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Process documents
async function processDocuments() {
    if (selectedFiles.length === 0) return;

    // Show progress
    progressSection.style.display = 'block';
    resultsSection.style.display = 'none';
    processBtn.disabled = true;

    try {
        const formData = new FormData();
        
        if (selectedFiles.length === 1) {
            // Single file upload
            formData.append('file', selectedFiles[0]);
            formData.append('enhance', enhanceCheckbox.checked);
            formData.append('output_format', outputFormat.value);

            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            extractedData = await response.json();
            
            // Debug: Log the response
            console.log('Server response:', extractedData);
            
            // Check if text was extracted
            if (!extractedData.text || extractedData.text.trim() === '') {
                throw new Error('No text was extracted from the document. The document may be empty or the OCR could not detect any text.');
            }
            
        } else {
            // Batch upload
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });
            formData.append('enhance', enhanceCheckbox.checked);

            const response = await fetch(`${API_BASE_URL}/batch-upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Batch upload failed');
            }

            const batchData = await response.json();
            
            // Combine results
            extractedData = {
                success: true,
                text: batchData.results.map(r => r.text).join('\n\n'),
                pages: batchData.results.length,
                pages_data: batchData.results.map((r, i) => ({
                    page: i + 1,
                    text: r.text,
                    char_count: r.char_count
                })),
                char_count: batchData.results.reduce((sum, r) => sum + (r.char_count || 0), 0),
                word_count: batchData.results.reduce((sum, r) => sum + (r.word_count || 0), 0)
            };
        }

        // Simulate progress
        animateProgress();

        // Wait for animation
        setTimeout(() => {
            displayResults();
            progressSection.style.display = 'none';
            showToast('Text extraction complete!', 'success');
        }, 2000);

    } catch (error) {
        console.error('Processing error:', error);
        showToast('Error processing documents. Please try again.', 'error');
        progressSection.style.display = 'none';
        processBtn.disabled = false;
    }
}

// Animate progress bar
function animateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        progressFill.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
    }, 200);
}

// Display results
function displayResults() {
    if (!extractedData) {
        console.error('No extracted data available');
        return;
    }

    console.log('Displaying results:', extractedData);

    // Update stats
    pageCount.textContent = extractedData.pages || 1;
    charCount.textContent = (extractedData.char_count || 0).toLocaleString();
    wordCount.textContent = (extractedData.word_count || 0).toLocaleString();

    // Display text
    if (extractedData.text) {
        textContent.textContent = extractedData.text;
    } else {
        textContent.textContent = 'No text was extracted from the document.';
    }

    // Display pages accordion if multiple pages
    if (extractedData.pages_data && extractedData.pages_data.length > 1) {
        pagesAccordion.innerHTML = extractedData.pages_data.map((page, index) => `
            <div class="page-item" data-page="${index}">
                <div class="page-header" onclick="togglePage(${index})">
                    <span class="page-title">
                        <i class="fas fa-file-alt"></i>
                        Page ${page.page} - ${page.char_count} characters
                    </span>
                    <i class="fas fa-chevron-down page-icon"></i>
                </div>
                <div class="page-content">
                    <div class="page-text">${page.text}</div>
                </div>
            </div>
        `).join('');
    } else {
        pagesAccordion.innerHTML = '';
    }

    // Show download PDF button if applicable
    if (extractedData.download_url) {
        downloadPdfBtn.style.display = 'inline-flex';
        downloadPdfBtn.setAttribute('data-url', extractedData.download_url);
    }

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Toggle page accordion
function togglePage(index) {
    const pageItem = document.querySelector(`.page-item[data-page="${index}"]`);
    pageItem.classList.toggle('active');
}

// Copy to clipboard
async function copyToClipboard() {
    try {
        await navigator.clipboard.writeText(extractedData.text);
        showToast('Text copied to clipboard!', 'success');
    } catch (error) {
        showToast('Failed to copy text', 'error');
    }
}

// Download as text
function downloadAsText() {
    if (!extractedData) return;

    const blob = new Blob([extractedData.text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'extracted_text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast('Text file downloaded!', 'success');
}

// Download as PDF
async function downloadAsPdf() {
    const downloadUrl = downloadPdfBtn.getAttribute('data-url');
    
    if (downloadUrl) {
        // Download from server
        window.open(`${API_BASE_URL}${downloadUrl}`, '_blank');
        showToast('PDF download started!', 'success');
    } else {
        showToast('PDF not available', 'error');
    }
}

// Reset app
function resetApp() {
    selectedFiles = [];
    extractedData = null;
    fileInput.value = '';
    renderFileList();
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    processBtn.disabled = true;
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show toast notification
function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    
    // Set color based on type
    if (type === 'error') {
        toast.style.background = '#ef4444';
    } else if (type === 'warning') {
        toast.style.background = '#f59e0b';
    } else {
        toast.style.background = '#10b981';
    }
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Smooth scrolling for navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active state
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Scroll to section
        const targetId = link.getAttribute('href');
        if (targetId === '#home') {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});
