#!/usr/bin/env python3
"""
Setup Verification Script for PDF Scanner with OCR
This script checks if all prerequisites are properly installed.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python():
    """Check Python installation"""
    print("\n🐍 Checking Python...")
    try:
        version = sys.version.split()[0]
        major, minor = map(int, version.split('.')[:2])
        
        if major >= 3 and minor >= 8:
            print(f"   ✅ Python {version} - OK")
            return True
        else:
            print(f"   ❌ Python {version} - Need 3.8 or higher")
            return False
    except Exception as e:
        print(f"   ❌ Error checking Python: {e}")
        return False

def check_tesseract():
    """Check Tesseract OCR installation"""
    print("\n📝 Checking Tesseract OCR...")
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   ✅ {version_line} - OK")
            return True
        else:
            print("   ❌ Tesseract found but error occurred")
            return False
    except FileNotFoundError:
        print("   ❌ Tesseract not found in PATH")
        print("   📥 Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    except Exception as e:
        print(f"   ❌ Error checking Tesseract: {e}")
        return False

def check_poppler():
    """Check Poppler installation"""
    print("\n📄 Checking Poppler (PDF support)...")
    try:
        result = subprocess.run(
            ['pdftoppm', '-v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Poppler outputs version to stderr
        version_output = result.stderr + result.stdout
        
        if 'poppler' in version_output.lower() or 'pdftoppm' in version_output.lower():
            print(f"   ✅ Poppler installed - OK")
            return True
        else:
            print("   ⚠️  Poppler found but version unclear")
            return True
    except FileNotFoundError:
        print("   ❌ Poppler not found in PATH")
        print("   📥 Install from: https://github.com/oschwartz10612/poppler-windows/releases/")
        return False
    except Exception as e:
        print(f"   ⚠️  Error checking Poppler: {e}")
        return False

def check_python_packages():
    """Check required Python packages"""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'PIL',
        'pytesseract',
        'pdf2image',
        'reportlab',
        'cv2',
        'numpy'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'PIL':
                __import__('PIL')
                print(f"   ✅ Pillow (PIL) - OK")
            elif package == 'cv2':
                __import__('cv2')
                print(f"   ✅ OpenCV (cv2) - OK")
            else:
                __import__(package)
                print(f"   ✅ {package} - OK")
        except ImportError:
            print(f"   ❌ {package} - NOT FOUND")
            all_installed = False
    
    if not all_installed:
        print("\n   💡 Install missing packages with:")
        print("      pip install -r requirements.txt")
    
    return all_installed

def check_directories():
    """Check required directories"""
    print("\n📁 Checking project directories...")
    
    required_dirs = ['uploads', 'outputs']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"   ✅ {dir_name}/ - OK")
        else:
            print(f"   ❌ {dir_name}/ - NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n   💡 Create directories with:")
        print("      mkdir uploads outputs")
    
    return all_exist

def check_files():
    """Check required files"""
    print("\n📄 Checking project files...")
    
    required_files = [
        'app.py',
        'index.html',
        'script.js',
        'style.css',
        'requirements.txt'
    ]
    
    all_exist = True
    
    for file_name in required_files:
        if os.path.exists(file_name) and os.path.isfile(file_name):
            print(f"   ✅ {file_name} - OK")
        else:
            print(f"   ❌ {file_name} - NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Main verification function"""
    print_header("PDF Scanner with OCR - Setup Verification")
    
    print("\nThis script will check if all prerequisites are properly installed.")
    print("Please wait while we verify your setup...\n")
    
    checks = {
        'Python': check_python(),
        'Tesseract': check_tesseract(),
        'Poppler': check_poppler(),
        'Python Packages': check_python_packages(),
        'Directories': check_directories(),
        'Project Files': check_files()
    }
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for name, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}")
    
    print(f"\n📊 Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! All prerequisites are installed.")
        print("\n🚀 You can start the application with:")
        print("   python app.py")
        print("\n   Then open index.html in your browser!")
    else:
        print("\n⚠️  Some prerequisites are missing.")
        print("\n📖 Please refer to INSTALLATION_GUIDE.md for detailed setup instructions.")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
