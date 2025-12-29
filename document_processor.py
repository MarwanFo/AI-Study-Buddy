"""
Document processing module for AI Study Buddy.
Phase 4: Multi-format support (.txt, .docx, .pdf)
"""

from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import re


# Supported file types
SUPPORTED_FORMATS = {
    'pdf': 'PDF Document',
    'txt': 'Text File',
    'docx': 'Word Document',
    'md': 'Markdown File'
}


def get_supported_formats() -> Dict[str, str]:
    """Get dictionary of supported file formats."""
    return SUPPORTED_FORMATS.copy()


def extract_text_from_file(uploaded_file) -> Tuple[str, Dict[int, str], str]:
    """
    Extract text from any supported file format.
    
    Phase 4: Unified extraction for PDF, TXT, DOCX, MD files.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Tuple of (full_text, page_map, file_type)
    """
    filename = uploaded_file.name.lower()
    
    if filename.endswith('.pdf'):
        text, page_map = extract_text_from_pdf_file(uploaded_file)
        return text, page_map, 'pdf'
    
    elif filename.endswith('.txt') or filename.endswith('.md'):
        text = extract_text_from_text_file(uploaded_file)
        # Text files don't have pages, treat as single page
        page_map = {1: text}
        return f"[Page 1]\n{text}", page_map, 'txt'
    
    elif filename.endswith('.docx'):
        text, page_map = extract_text_from_docx_file(uploaded_file)
        return text, page_map, 'docx'
    
    else:
        ext = Path(filename).suffix
        raise ValueError(f"Unsupported file format: {ext}. Supported: {', '.join(SUPPORTED_FORMATS.keys())}")


def extract_text_from_pdf_file(uploaded_file) -> Tuple[str, Dict[int, str]]:
    """Extract text from a PDF file."""
    from pypdf import PdfReader
    import io
    
    try:
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        
        if len(pdf_reader.pages) == 0:
            raise ValueError("PDF has no pages")
        
        text_parts = []
        page_map = {}
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                page_text = page.extract_text()
                if page_text:
                    cleaned_text = clean_text(page_text)
                    page_map[page_num] = cleaned_text
                    text_parts.append(f"\n[Page {page_num}]\n{cleaned_text}")
            except Exception as e:
                print(f"  ⚠️ Warning: Could not extract page {page_num}: {e}")
                continue
        
        full_text = "\n".join(text_parts)
        
        if not full_text.strip():
            raise ValueError("PDF contains no extractable text. It might be scanned images.")
        
        uploaded_file.seek(0)
        return full_text, page_map
        
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Failed to process PDF: {str(e)}")


def extract_text_from_text_file(uploaded_file) -> str:
    """Extract text from a .txt or .md file."""
    try:
        content = uploaded_file.read()
        
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                text = content.decode(encoding)
                uploaded_file.seek(0)
                return clean_text(text)
            except UnicodeDecodeError:
                continue
        
        raise ValueError("Could not decode text file. Unsupported encoding.")
        
    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


def extract_text_from_docx_file(uploaded_file) -> Tuple[str, Dict[int, str]]:
    """
    Extract text from a .docx file.
    Phase 4: Word document support.
    """
    try:
        from docx import Document
        import io
        
        doc = Document(io.BytesIO(uploaded_file.read()))
        
        paragraphs = []
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text.strip())
        
        if not paragraphs:
            raise ValueError("Word document contains no text")
        
        # Estimate pages (roughly 3000 chars per page)
        full_text = "\n\n".join(paragraphs)
        chars_per_page = 3000
        
        page_map = {}
        text_parts = []
        current_page = 1
        current_chars = 0
        current_page_text = []
        
        for para in paragraphs:
            current_page_text.append(para)
            current_chars += len(para)
            
            if current_chars >= chars_per_page:
                page_text = "\n\n".join(current_page_text)
                page_map[current_page] = page_text
                text_parts.append(f"\n[Page {current_page}]\n{page_text}")
                current_page += 1
                current_chars = 0
                current_page_text = []
        
        # Last page
        if current_page_text:
            page_text = "\n\n".join(current_page_text)
            page_map[current_page] = page_text
            text_parts.append(f"\n[Page {current_page}]\n{page_text}")
        
        uploaded_file.seek(0)
        return "\n".join(text_parts), page_map
        
    except ImportError:
        raise ValueError("python-docx not installed. Run: pip install python-docx")
    except Exception as e:
        raise ValueError(f"Failed to read Word document: {str(e)}")


def clean_text(text: str) -> str:
    """Clean extracted text by removing extra whitespace and artifacts."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text.strip()


def smart_chunk_text(
    text: str,
    page_map: Dict[int, str],
    document_name: str,
    chunk_size: int = 400,
    chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """
    Smart semantic chunking that respects paragraph boundaries.
    """
    if not text or not text.strip():
        return []
    
    chunks = []
    current_page = 1
    
    paragraphs = re.split(r'\n\n+', text)
    
    current_chunk = ""
    current_chunk_page = 1
    
    for para in paragraphs:
        page_match = re.match(r'\[Page (\d+)\]', para)
        if page_match:
            current_page = int(page_match.group(1))
            para = re.sub(r'\[Page \d+\]\s*', '', para)
        
        para = para.strip()
        if not para:
            continue
        
        if len(current_chunk) + len(para) + 1 <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
                current_chunk_page = current_page
        else:
            if current_chunk.strip():
                chunks.append({
                    'text': current_chunk.strip(),
                    'page': current_chunk_page,
                    'document': document_name
                })
            
            if len(para) > chunk_size:
                sentence_chunks = _split_long_paragraph(
                    para, current_page, document_name, chunk_size, chunk_overlap
                )
                chunks.extend(sentence_chunks)
                current_chunk = ""
            else:
                if current_chunk and chunk_overlap > 0:
                    overlap = _get_overlap_text(current_chunk, chunk_overlap)
                    current_chunk = overlap + "\n\n" + para
                else:
                    current_chunk = para
                current_chunk_page = current_page
    
    if current_chunk.strip():
        chunks.append({
            'text': current_chunk.strip(),
            'page': current_chunk_page,
            'document': document_name
        })
    
    return chunks


def _split_long_paragraph(
    paragraph: str,
    page: int,
    document: str,
    chunk_size: int,
    overlap: int
) -> List[Dict[str, Any]]:
    """Split a long paragraph by sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    
    chunks = []
    current = ""
    
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= chunk_size:
            current = current + " " + sentence if current else sentence
        else:
            if current.strip():
                chunks.append({
                    'text': current.strip(),
                    'page': page,
                    'document': document
                })
            
            if current and overlap > 0:
                overlap_text = _get_overlap_text(current, overlap)
                current = overlap_text + " " + sentence
            else:
                current = sentence
    
    if current.strip():
        chunks.append({
            'text': current.strip(),
            'page': page,
            'document': document
        })
    
    return chunks


def _get_overlap_text(text: str, overlap_chars: int) -> str:
    """Get the last N characters for overlap, breaking at word boundary."""
    if len(text) <= overlap_chars:
        return text
    
    overlap_text = text[-overlap_chars:]
    space_idx = overlap_text.find(' ')
    if space_idx > 0:
        overlap_text = overlap_text[space_idx + 1:]
    
    return overlap_text


# Backward compatibility aliases
def extract_text_from_uploaded_file(uploaded_file) -> Tuple[str, Dict[int, str]]:
    """Legacy function - use extract_text_from_file instead."""
    text, page_map, _ = extract_text_from_file(uploaded_file)
    return text, page_map


def chunk_text_with_metadata(
    text: str,
    page_map: Dict[int, str],
    document_name: str,
    chunk_size: int = 400,
    chunk_overlap: int = 100
) -> List[Dict[str, Any]]:
    """Alias for smart_chunk_text."""
    return smart_chunk_text(text, page_map, document_name, chunk_size, chunk_overlap)
