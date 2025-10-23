"""
Simplified Document Processing Utility for Vercel
Extract text content from basic document formats
"""

import os
import io
import uuid
from typing import Dict, List, Optional, Tuple
from werkzeug.utils import secure_filename

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

def process_document(file_path: str, filename: str) -> Dict[str, Any]:
    """
    Process a document and extract text content
    
    Args:
        file_path: Path to the uploaded file
        filename: Original filename
        
    Returns:
        Dictionary containing extracted content and metadata
    """
    result = {
        'success': False,
        'content': '',
        'word_count': 0,
        'extraction_method': 'none',
        'file_type': get_file_type(filename),
        'error': None
    }
    
    try:
        file_type = get_file_type(filename)
        
        if file_type == 'pdf':
            result = process_pdf(file_path)
        elif file_type == 'docx':
            result = process_docx(file_path)
        elif file_type == 'txt':
            result = process_text(file_path)
        elif file_type == 'md':
            result = process_markdown(file_path)
        else:
            result['error'] = f'Unsupported file type: {file_type}'
            
    except Exception as e:
        result['error'] = f'Error processing document: {str(e)}'
    
    return result

def get_file_type(filename: str) -> str:
    """Get file type from filename"""
    ext = os.path.splitext(filename)[1].lower()
    type_map = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'docx',
        '.txt': 'txt',
        '.md': 'md',
        '.rtf': 'rtf'
    }
    return type_map.get(ext, 'unknown')

def process_pdf(file_path: str) -> Dict[str, Any]:
    """Process PDF file"""
    result = {
        'success': False,
        'content': '',
        'word_count': 0,
        'extraction_method': 'none',
        'file_type': 'pdf',
        'error': None
    }
    
    try:
        if PDFPLUMBER_AVAILABLE:
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    result['content'] = text.strip()
                    result['extraction_method'] = 'pdfplumber'
                    result['success'] = True
                else:
                    result['error'] = 'No text could be extracted from PDF'
        elif PDF_AVAILABLE:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if text.strip():
                    result['content'] = text.strip()
                    result['extraction_method'] = 'PyPDF2'
                    result['success'] = True
                else:
                    result['error'] = 'No text could be extracted from PDF'
        else:
            result['error'] = 'PDF processing libraries not available'
            
    except Exception as e:
        result['error'] = f'Error processing PDF: {str(e)}'
    
    if result['success']:
        result['word_count'] = len(result['content'].split())
    
    return result

def process_docx(file_path: str) -> Dict[str, Any]:
    """Process DOCX file"""
    result = {
        'success': False,
        'content': '',
        'word_count': 0,
        'extraction_method': 'none',
        'file_type': 'docx',
        'error': None
    }
    
    try:
        if DOCX_AVAILABLE:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            if text.strip():
                result['content'] = text.strip()
                result['extraction_method'] = 'python-docx'
                result['success'] = True
                result['word_count'] = len(text.split())
            else:
                result['error'] = 'No text found in document'
        else:
            result['error'] = 'DOCX processing library not available'
            
    except Exception as e:
        result['error'] = f'Error processing DOCX: {str(e)}'
    
    return result

def process_text(file_path: str) -> Dict[str, Any]:
    """Process text file"""
    result = {
        'success': False,
        'content': '',
        'word_count': 0,
        'extraction_method': 'none',
        'file_type': 'txt',
        'error': None
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                result['content'] = content.strip()
                result['extraction_method'] = 'text'
                result['success'] = True
                result['word_count'] = len(content.split())
            else:
                result['error'] = 'File is empty'
                
    except Exception as e:
        result['error'] = f'Error processing text file: {str(e)}'
    
    return result

def process_markdown(file_path: str) -> Dict[str, Any]:
    """Process markdown file"""
    result = {
        'success': False,
        'content': '',
        'word_count': 0,
        'extraction_method': 'none',
        'file_type': 'md',
        'error': None
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                result['content'] = content.strip()
                result['extraction_method'] = 'markdown'
                result['success'] = True
                result['word_count'] = len(content.split())
            else:
                result['error'] = 'File is empty'
                
    except Exception as e:
        result['error'] = f'Error processing markdown file: {str(e)}'
    
    return result

def format_content(content: str, file_type: str) -> str:
    """Format content for display"""
    if not content:
        return ""
    
    if file_type == 'md':
        if MARKDOWN_AVAILABLE:
            html = markdown.markdown(content)
            return html
        else:
            return content.replace('\n', '<br>')
    else:
        return content.replace('\n', '<br>')
