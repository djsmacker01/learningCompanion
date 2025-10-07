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

try:
    import pytesseract
    from PIL import Image
    import fitz  # PyMuPDF
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

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
        text_content = ""
        pages_info = []
        extraction_method = "none"
        
        try:
            # First try standard text extraction
            if PDFPLUMBER_AVAILABLE:
                print("Attempting pdfplumber extraction...")
                text_content, pages_info = self._extract_with_pdfplumber(file_path)
                extraction_method = "pdfplumber"
                print(f"Pdfplumber extracted {len(text_content)} characters from {len(pages_info)} pages")
            elif PDF_AVAILABLE:
                print("Attempting PyPDF2 extraction...")
                text_content, pages_info = self._extract_with_pypdf2(file_path)
                extraction_method = "pypdf2"
                print(f"PyPDF2 extracted {len(text_content)} characters from {len(pages_info)} pages")
            elif PDFMINER_AVAILABLE:
                print("Attempting pdfminer extraction...")
                text_content, pages_info = self._extract_with_pdfminer(file_path)
                extraction_method = "pdfminer"
                print(f"Pdfminer extracted {len(text_content)} characters from {len(pages_info)} pages")
            
            # If no text extracted, try OCR for image-based PDFs
            if not text_content.strip() and OCR_AVAILABLE:
                print("No text found, attempting OCR extraction...")
                ocr_result = self._extract_with_ocr(file_path)
                if ocr_result['success']:
                    text_content = ocr_result['text_content']
                    pages_info = ocr_result['pages_info']
                    extraction_method = "ocr"
                    print(f"OCR extracted {len(text_content)} characters")
            
            # If still no content, return helpful error message
            if not text_content.strip():
                error_message = "No extractable text found in PDF."
                if extraction_method == "pdfplumber" or extraction_method == "pypdf2":
                    error_message += " This appears to be an image-based PDF (scanned document)."
                if not OCR_AVAILABLE:
                    error_message += " OCR (Optical Character Recognition) is not available to extract text from images."
                else:
                    error_message += " OCR extraction failed - Tesseract may not be properly installed."
                
                return {
                    'success': False,
                    'error': error_message,
                    'text_content': '',
                    'pages_info': pages_info,
                    'extraction_method': extraction_method,
                    'is_image_based': True,
                    'suggestions': [
                        "Try uploading a PDF with selectable text instead of a scanned image",
                        "Install Tesseract OCR for image-based PDF support",
                        "Convert the PDF to a text-based format before uploading"
                    ]
                }
            
            # Process the extracted text
            processed_content = self._process_extracted_text(text_content, extraction_method)
            
            return {
                'success': True,
                'text_content': processed_content['cleaned_text'],
                'pages_info': pages_info,
                'word_count': processed_content['word_count'],
                'key_sections': processed_content['key_sections'],
                'extraction_method': extraction_method
            }
            
        except Exception as e:
            print(f"Critical error in PDF extraction: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Critical error extracting PDF content: {str(e)}',
                'text_content': text_content,
                'pages_info': pages_info,
                'extraction_method': extraction_method if 'extraction_method' in locals() else 'error'
            }
    
    def _extract_with_pdfplumber(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using pdfplumber (most reliable)"""
        try:
            text_content = ""
            pages_info = []
            
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # Try to extract text with better formatting preservation
                        page_text = page.extract_text(layout=True)
                        if not page_text:
                            # Fallback to regular extraction
                            page_text = page.extract_text()
                        
                        if page_text:
                            # Clean up the text but preserve structure
                            page_text = self._clean_pdf_page_text(page_text)
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
                    except Exception as page_error:
                        print(f"Error extracting text from page {page_num}: {page_error}")
                        pages_info.append({
                            'page_number': page_num,
                            'text_length': 0,
                            'word_count': 0,
                            'has_text': False,
                            'error': str(page_error)
                        })
            
            return text_content, pages_info
            
        except Exception as e:
            print(f"Error with pdfplumber extraction: {e}")
            return "", []
    
    def _clean_pdf_page_text(self, text: str) -> str:
        """Clean PDF page text while preserving structure"""
        import re
        
        if not text:
            return ""
        
        # Split into lines
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                cleaned_lines.append("")
                continue
            
            # Remove excessive whitespace
            line = re.sub(r'\s+', ' ', line)
            
            # Remove common PDF artifacts
            line = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\'\"\/\@\#\&\+\=]+', ' ', line)
            
            # Clean up multiple spaces again
            line = re.sub(r'\s+', ' ', line)
            
            # Skip lines that are just page numbers or headers
            if re.match(r'^\d+$', line) or len(line) < 3:
                continue
                
            cleaned_lines.append(line)
        
        # Join lines and clean up excessive empty lines
        result = '\n'.join(cleaned_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result.strip()
    
    def _extract_with_pypdf2(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using PyPDF2"""
        try:
            text_content = ""
            pages_info = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
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
                    except Exception as page_error:
                        print(f"Error extracting text from page {page_num} with PyPDF2: {page_error}")
                        pages_info.append({
                            'page_number': page_num,
                            'text_length': 0,
                            'word_count': 0,
                            'has_text': False,
                            'error': str(page_error)
                        })
            
            return text_content, pages_info
            
        except Exception as e:
            print(f"Error with PyPDF2 extraction: {e}")
            return "", []
    
    def _extract_with_pdfminer(self, file_path: str) -> Tuple[str, List[Dict]]:
        """Extract text using pdfminer"""
        try:
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
            
        except Exception as e:
            print(f"Error with pdfminer extraction: {e}")
            return "", []
    
    def _extract_with_ocr(self, file_path: str) -> Dict:
        """Extract text using OCR for image-based PDFs"""
        try:
            import pytesseract
            from PIL import Image
            import fitz  # PyMuPDF
            
            text_content = ""
            pages_info = []
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(file_path)
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Convert PDF page to image
                mat = fitz.Matrix(2.0, 2.0)  # Scale factor for better OCR
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("png")
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(img_data))
                
                # Extract text using OCR
                page_text = pytesseract.image_to_string(image, lang='eng')
                
                if page_text.strip():
                    text_content += page_text + "\n\n"
                    pages_info.append({
                        'page_number': page_num + 1,
                        'text_length': len(page_text),
                        'word_count': len(page_text.split()),
                        'has_text': True,
                        'extraction_method': 'ocr'
                    })
                else:
                    pages_info.append({
                        'page_number': page_num + 1,
                        'text_length': 0,
                        'word_count': 0,
                        'has_text': False,
                        'extraction_method': 'ocr'
                    })
            
            pdf_document.close()
            
            return {
                'success': True,
                'text_content': text_content,
                'pages_info': pages_info
            }
            
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return {
                'success': False,
                'text_content': "",
                'pages_info': [],
                'error': str(e)
            }
    
    def _process_extracted_text(self, text_content: str, extraction_method: str = 'unknown') -> Dict:
        """Process and clean extracted text"""
        if not text_content:
            return {
                'cleaned_text': '',
                'word_count': 0,
                'key_sections': [],
                'extraction_method': extraction_method
            }
        
        # Clean the text
        cleaned_text = self._clean_text(text_content)
        
        # Extract key sections
        key_sections = self._extract_key_sections(cleaned_text)
        
        return {
            'cleaned_text': cleaned_text,
            'word_count': len(cleaned_text.split()),
            'key_sections': key_sections,
            'extraction_method': extraction_method
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text while preserving structure"""
        import re
        
        if not text:
            return ""
        
        # Split into lines for better processing
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                # Preserve empty lines for structure
                cleaned_lines.append("")
                continue
            
            # Remove excessive spaces but keep single spaces
            line = re.sub(r'\s+', ' ', line)
            
            # Remove special characters that aren't useful but keep punctuation
            line = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\'\"]+', ' ', line)
            
            # Clean up multiple spaces again
            line = re.sub(r'\s+', ' ', line)
            
            # Skip lines that are just page numbers or very short
            if re.match(r'^\d+$', line) or len(line) < 3:
                continue
                
            cleaned_lines.append(line)
        
        # Join lines and clean up excessive empty lines
        result = '\n'.join(cleaned_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        # Add better structure detection
        result = self._add_structure_markers(result)
        
        return result.strip()
    
    def _add_structure_markers(self, text: str) -> str:
        """Add structure markers to improve formatting"""
        import re
        
        lines = text.split('\n')
        structured_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                structured_lines.append("")
                continue
            
            # Detect potential headings (short lines, title case, or all caps)
            if (len(line) < 100 and 
                (line.isupper() or line.istitle()) and 
                not line.endswith('.') and 
                not line.endswith(',') and
                not re.match(r'^\d+\.?\s', line)):  # Not numbered lists
                # Likely a heading
                structured_lines.append("")
                structured_lines.append(line)
                structured_lines.append("-" * min(len(line), 50))
                structured_lines.append("")
            else:
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)
    
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
        return PDFPLUMBER_AVAILABLE or PDF_AVAILABLE or PDFMINER_AVAILABLE or OCR_AVAILABLE
    
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
        if not OCR_AVAILABLE:
            libraries.append('pytesseract')
            libraries.append('PyMuPDF')
        return libraries
