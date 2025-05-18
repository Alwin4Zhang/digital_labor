from .unstructured_loaders.doc_loader import DocLoader
from .unstructured_loaders.pdf_loader import PDFLoader
from .unstructured_loaders.ppt_loader import PPTLoader
from .unstructured_loaders.table_loader import TableLoader
from .unstructured_loaders.qa_loader import QALoader

__all__ = ["DocLoader", "PDFLoader", "PPTLoader", "TableLoader","QALoader"]
