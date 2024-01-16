__version__ = "0.1.0"

from .config import PageConfig
from .pdf_generator import PDFGenerator

__all__ = ["PDFGenerator", "PageConfig"]
