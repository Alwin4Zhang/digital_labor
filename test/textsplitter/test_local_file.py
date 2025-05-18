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


if __name__ == "__main__":
    local_file_path = "/Users/ucdteam/Downloads/解析失败文件/THSY-2024-02天虹股份在营商业项目EHS评估综合报告-吉安天虹.pdf"
    doc_loader = PDFLoader(file_path=local_file_path, file_stream=None)
    blocks = doc_loader.blocks
    full_content = ""
    for block in blocks:
        print(block)
        # print(block['markdown'])
        # full_content += block['markdown'] + "\n"

    from langchain_openai import ChatOpenAI

    # print(blocks)
