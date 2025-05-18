import sys
import re

sys.path.append("./")

from typing import (
    AbstractSet,
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypedDict,
    TypeVar,
    Union,
    cast,
)

import numpy as np
from langchain.docstore.document import Document

from configs.model_config import CHUNK_SIZE
from loader.unstructured_loaders.constants import (
    heading_levels,
    NORMAL,
    HEADING1,
    HEADING2,
)

from utils.llm_util import get_num_tokens_from_messages

class CommonchsDocSplitter():
    
    def __init__(self,chunk_size=CHUNK_SIZE) -> None:
        self.chunk_size = chunk_size
        
    def split_text(self,blocks):        
        documents = []
        chunk,chunk_html,chunk_md = [],[],[]
        
        for i,block in enumerate(blocks):
            data = block["data"]
            style = block["style"]
            html = block["html"]
            md = block.get("markdown", "")
            # 图片添加ocr识别的内容
            text = block.get("text","")
            
            stripped_line = ""
            if style.lower() not in ["image", "table"]:
                stripped_line = data.strip()
            if style.lower() in ["table"]:
                stripped_line = md
            if style.lower() in ["image"]:
                if text:
                    stripped_line = text + "\n\n" + md
                else:
                    stripped_line = md
            chunk.append(stripped_line)
            chunk_html.append(html)
            chunk_md.append(md)
            
            if get_num_tokens_from_messages(content='\n'.join(chunk)) >=  self.chunk_size or i == len(blocks) - 1:               
                documents.append(
                    Document(page_content='\n'.join(chunk),metadata={
                    "html": ''.join(chunk_html),
                    "markdown": "\n\n".join(chunk_md)
                }))
                chunk,chunk_html,chunk_md = [],[],[]                
        return documents
    
    
commonchs_doc_splitter = CommonchsDocSplitter()