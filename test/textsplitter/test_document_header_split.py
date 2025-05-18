import sys
import json

sys.path.append("./")

from io import BytesIO, StringIO

from loader.unstructured_loaders.pdf_loader import PDFLoader
from loader.unstructured_loaders.doc_loader import DocLoader
from loader.unstructured_loaders.qa_loader import TableLoader
from loader.unstructured_loaders.ppt_loader import PPTLoader
from textsplitter.document_header_splitter import DocumentHeaderTextSplitter
from utils.common import convert_bytes_to_file, convert_file_type


doc_splitter = DocumentHeaderTextSplitter()

if __name__ == "__main__":
    abs_path = "./test/test_files/操作教程.pdf"
    pdf_loader = PDFLoader(
        file_path=abs_path
    )
    
    blocks = pdf_loader.blocks
    
    documents = doc_splitter.split_text(blocks=blocks[:])
    print(documents)
