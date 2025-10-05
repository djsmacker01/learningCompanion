"""
PDF Processing Utility
Extract text content from PDF files and process them for study materials
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
    from pdfminer.high_level import extract_text
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False

class PDFProcessor:
    """PDF content extraction and processing utility"""
    
    def __init__(self):
        self.upload_dir = "uploads"
        self._ensure_upload_dir()
    
    def _ensure_upload_dir(self):
        """Ensure upload directory exists"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    def extract_text_from_pdf(self, file_path: str) -> Dict:
        """Extract text content from PDF file"""
        try:
            text_content = ""
            pages_info = []
            
            # Try multiple PDF extraction methods
            if PDFPLUMBER_AVAILABLE:
                text_content, pages_info = self._extract_with_pdfplumber(file_path)
            elif PyPDF2 and PDF_AVAILABLE:
                text_content, pages_info = self._extract_with_pypdf2(file_path)
            elif PDFMINER_AVAILABLE:
                text_content, pages_info = self._extract_with_pdfminer(file_path)
            else:
                return {
                    'success': False,
                    'error': 'No PDF processing libraries available. Please install PyPDF2, pdfplumber, or pdfminer',
                    'text_content': '',
                    'pages_info': []
                }
            
            # Process the extracted text
            processed_content = self._process_extracted_text(text_content)
            
            return {
                'success': True,
                'text_content': processed_content['cleaned_text'],
                'pages_info': pages_info,
                'word_count': processed_content['word_count'],
                'key_sections': processed_content['key_sections'],
                'extraction_method': processed_content['extraction_method']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting PDF content: {str(e)}',
                'text_content': '',
                'pages_info': []
            }
    
    def _extract_with_pdfplumber(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using pdfplumber (most reliable)"""
        text_content = ""
        pages_info = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n\n"
                    pages_info.append({
                        'page_number': page_num,
                        'text_length': len(page_text),
                        'word_count': len(page_text.split()),
                        'has_text': True
                    })
                else:
                    pages_info.append({
                        'page_number': page_num,
                        'text_length': 0,
                        'word_count': 0,
                        'has_text': False
                    })
        
        return text_content, pages_info
    
    def _extract_with_pypdf2(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using PyPDF2"""
        text_content = ""
        pages_info = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n\n"
                    pages_info.append({
                        'page_number': page_num,
                        'text_length': len(page_text),
                        'word_count': len(page_text.split()),
                        'has_text': True
                    })
                else:
                    pages_info.append({
                        'page_number': page_num,
                        'text_length': 0,
                        'word_count': 0,
                        'has_text': False
                    })
        
        return text_content, pages_info
    
    def _extract_with_pdfminer(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using pdfminer"""
        text_content = extract_text(file_path)
        
        # Split by pages (approximate)
        pages = text_content.split('\f')  # Form feed character
        pages_info = []
        
        for page_num, page_text in enumerate(pages, 1):
            if page_text.strip():
                pages_info.append({
                    'page_number': page_num,
                    'text_length': len(page_text),
                    'word_count': len(page_text.split()),
                    'has_text': True
                })
            else:
                pages_info.append({
                    'page_number': page_num,
                    'text_length': 0,
                    'word_count': 0,
                    'has_text': False
                })
        
        return text_content, pages_info
    
    def _process_extracted_text(self, text_content: str) -> Dict:
        """Process and clean extracted text"""
        if not text_content:
            return {
                'cleaned_text': '',
                'word_count': 0,
                'key_sections': [],
                'extraction_method': 'none'
            }
        
        # Clean the text
        cleaned_text = self._clean_text(text_content)
        
        # Extract key sections
        key_sections = self._extract_key_sections(cleaned_text)
        
        # Determine extraction method used
        extraction_method = "pdfplumber" if PDFPLUMBER_AVAILABLE else (
            "pypdf2" if PDF_AVAILABLE else (
                "pdfminer" if PDFMINER_AVAILABLE else "none"
            )
        )
        
        return {
            'cleaned_text': cleaned_text,
            'word_count': len(cleaned_text.split()),
            'key_sections': key_sections,
            'extraction_method': extraction_method
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers (common patterns)
        text = re.sub(r'\b\d+\b(?=\s*$)', '', text, flags=re.MULTILINE)  # Page numbers at end of line
        text = re.sub(r'^.*\b\d+\b\s*$', '', text, flags=re.MULTILINE)   # Lines with only numbers
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\'\"]+', ' ', text)  # Keep punctuation but remove special chars
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def _extract_key_sections(self, text: str) -> List[Dict]:
        """Extract key sections from the text"""
        import re
        
        sections = []
        
        # Look for common section patterns
        section_patterns = [
            r'(Chapter\s+\d+[:\s]+[^\n]+)',
            r'(Section\s+\d+[:\s]+[^\n]+)',
            r'(^\d+\.\s+[^\n]+)',  # Numbered sections
            r'(^[A-Z][A-Z\s]{2,}:)',  # All caps headings
            r'(^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*:)',  # Title case headings
        ]
        
        for pattern in section_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                if len(match.strip()) > 3:  # Avoid very short matches
                    sections.append({
                        'title': match.strip(),
                        'type': 'heading'
                    })
        
        # Look for key terms (words that appear frequently)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only longer words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add frequent terms as key concepts
        for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
            if freq > 2:  # Only terms that appear multiple times
                sections.append({
                    'title': word,
                    'type': 'concept',
                    'frequency': freq
                })
        
        return sections
    
    def save_uploaded_file(self, file) -> Dict:
        """Save uploaded file and return file info"""
        try:
            # Generate secure filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Get file info
            file_size = os.path.getsize(file_path)
            
            return {
                'success': True,
                'file_path': file_path,
                'filename': unique_filename,
                'original_filename': file.filename,
                'file_size': file_size,
                'file_type': filename.split('.')[-1].lower() if '.' in filename else 'unknown'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error saving file: {str(e)}'
            }
    
    def process_uploaded_pdf(self, file) -> Dict:
        """Complete PDF processing pipeline"""
        try:
            # Save the file
            save_result = self.save_uploaded_file(file)
            if not save_result['success']:
                return save_result
            
            # Check if it's a PDF
            if save_result['file_type'] != 'pdf':
                return {
                    'success': False,
                    'error': 'File is not a PDF',
                    'file_info': save_result
                }
            
            # Extract text content
            extraction_result = self.extract_text_from_pdf(save_result['file_path'])
            
            # Combine results
            result = {
                'success': extraction_result['success'],
                'file_info': save_result,
                'content_info': extraction_result
            }
            
            # Add error if extraction failed
            if not extraction_result['success']:
                result['error'] = extraction_result['error']
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing PDF: {str(e)}'
            }
    
    @staticmethod
    def is_pdf_processing_available() -> bool:
        """Check if PDF processing libraries are available"""
        return PDFPLUMBER_AVAILABLE or PDF_AVAILABLE or PDFMINER_AVAILABLE
    
    @staticmethod
    def get_required_libraries() -> List[str]:
        """Get list of required PDF processing libraries"""
        libraries = []
        if not PDFPLUMBER_AVAILABLE:
            libraries.append('pdfplumber')
        if not PDF_AVAILABLE:
            libraries.append('PyPDF2')
        if not PDFMINER_AVAILABLE:
            libraries.append('pdfminer.six')
        return libraries
