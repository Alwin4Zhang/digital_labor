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

from loader.unstructured_loaders.constants import (
    heading_levels,
    NORMAL,
    HEADING1,
    HEADING2,
)
from configs.model_config import embedding_model_dict
from db.embedding_utils import embed_texts_api

# from langchain.text_splitter import MarkdownHeaderTextSplitter
from configs.model_config import SENTENCE_SIZE
from utils.string_util import remove_punctuation

# from textsplitter.chinese_text_splitter import ChineseTextSplitter

# chinese_textsplitter = ChineseTextSplitter()

class LineType(TypedDict):
    """Line type as typed dict."""

    metadata: Dict[str, str]
    content: str
    html: str


class HeaderType(TypedDict):
    """Header type as typed dict."""

    level: int
    name: str
    data: str
    html: str


class DocumentHeaderTextSplitter:
    """Splitting mardown files based on specified headers"""
    MILVUS_CHUNK_MAX_LENGTH = 65535 # milvus最长文本长度限制

    def __init__(
        self,
        headers_to_split_on: List[str] = [
            "Title",
            "Heading 1",
            "Heading 2",
            "Heading 3",
            "Heading 4",
            "Heading 5",
            "Heading 6",
            "Normal",
        ]
    ):

        # (e.g., "Heading1, Heading2, etc") order by value
        self.headers_to_split_on = sorted(
            headers_to_split_on, key=lambda x: heading_levels[x]
        )
        self.min_priority_level = heading_levels[
            sorted(headers_to_split_on, key=lambda x: heading_levels[x])[-1]
        ]
        
        self.model_pipeline = None
        

    def document_segment(self, text):
        if not self.model_pipeline:
            from modelscope import pipeline
            from modelscope.preprocessors import Preprocessor
            from modelscope.models import Model

            model = Model.from_pretrained(
                model_name_or_path=embedding_model_dict["document-segmentation"]
            )
            self.model_pipeline = pipeline(
                task="document-segmentation", model=model, device="cpu"
            )
        result = self.model_pipeline(documents=text)
        sent_list = [i for i in result["text"].split("\n\t") if i]
        return sent_list

    def split_text(
        self,
        blocks: List,
        use_modelscope: bool = False,
        use_semantic: bool = False,
        use_header: bool = False,
    ) -> List[Document]:
        """多模态chunk拆分"""
        data_tuples = [
            (block["data"], block["style"], block["html"], block.get("markdown", ""))
            for block in blocks
        ]
        data_processed_tuples = []
        for data, style, html, md in data_tuples:
            current_level = heading_levels.get(style, 10)
            data_processed_tuples.append((data, style, html, md))
        # Final output
        lines_with_metadata: List[LineType] = []

        # Keep track of the nested header structure
        header_stack: List[HeaderType] = []
        initial_metadata: Dict[str, str] = {}

        for data, style, html, md in data_processed_tuples:
            stripped_line = ""
            if style.lower() not in ["image", "table"]:
                stripped_line = data.strip()
            if style.lower() in ["table"]:
                stripped_line = md
            if style.lower() in ["image"]:
                stripped_line = md

            # check each line against each of the header types (e.g, Heading1,Heading2)
            current_level = heading_levels.get(style, 10)
            """
            # 1.header_stack有且更低等级
            # 2.
                2.1 如果不是正文，break
                2.2 如果是正文，出栈拼接内容
            # 3. current header push to stack
            # 4. 当前不是正文,获取比当前level更高的所有header level
            # 5. 当前的level替换原有的同级level,比如：当前是h1,上一个也是h1，就替换当前的level
            """
            while header_stack and header_stack[-1]["level"] > current_level:
                # 当前stack
                if header_stack[-1]["level"] != self.min_priority_level:
                    break

                content = ""
                parsed_html = ""
                parsed_markdown = ""
                while (
                    header_stack
                    and header_stack[-1]["level"] == self.min_priority_level
                ):  # 拼接当前的content
                    cur = header_stack.pop()
                    content = cur["data"] + content
                    parsed_html = cur["html"] + parsed_html
                    parsed_markdown = cur["markdown"] + parsed_markdown
                    cur_style = cur["name"]
                if use_modelscope:
                    lines = self.document_segment(content)
                    for line in lines:
                        lines_with_metadata.append(
                            {"content": line, "metadata": initial_metadata.copy()}
                        )
                else:
                    lines_with_metadata.append(
                        {
                            "content": content,
                            "html": parsed_html,
                            "markdown": parsed_markdown,
                            "metadata": initial_metadata.copy(),
                        }
                    )

            header: HeaderType = {
                "level": current_level,
                "name": style,
                "data": stripped_line,
                "html": html,
                "markdown": md,
            }
            header_stack.append(header)
            if current_level < self.min_priority_level:
                if style in initial_metadata:
                    initial_metadata_copy = {}
                    temp = []  # temp存储是同等级的headers
                    for k, v in initial_metadata.items():
                        k_level = heading_levels[k]
                        if k_level <= current_level:
                            initial_metadata_copy[k] = v
                        if k_level == current_level:
                            temp.append(k)

                    initial_metadata = initial_metadata_copy.copy()

                # initial_metadata[style] = header["data"]

                initial_metadata[style] = {
                    "data": header["data"],
                    "html": header["html"],
                    "markdown": header["markdown"],
                }
                
        # TDOO:清洗拆分各种类型的拆分策略
        """
        定位是智能拆分，且能兼容原有的强依赖header的拆分策略
        1.主要是片段明确header 
        2.合并策略：
            (1) 按照chunk_size拆分，使用tiktoken统计字符;
            (2) 每个chunk的metadata带有header的信息
        """
        
        # Group By Header
        content = ""
        parsed_html = ""
        parsed_markdown = ""
        while header_stack and header_stack[-1]["level"] == self.min_priority_level:
            cur = header_stack.pop()
            cur_style = cur["name"]
            parsed_html = cur["html"] + parsed_html
            cur_md = cur["markdown"]
            cur_data = cur["data"]
            if cur_style == "image":
                cur_md += "\\n"  # confused 图片后面加一个换行符，避免连续的markdown图片链接问答时产生影响
                cur_data = cur_md
            content = cur_data + "\n\n" + content
            parsed_markdown = cur_md + "\n\n" + parsed_markdown

        if use_modelscope:
            lines = self.document_segment(content)
            for line in lines:
                lines_with_metadata.append(
                    {"content": line, "metadata": initial_metadata.copy()}
                )
        else:
            lines_with_metadata.append(
                {
                    "content": content,
                    "html": parsed_html,
                    "markdown": parsed_markdown,
                    "metadata": initial_metadata.copy(),
                }
            )
        documents = []
        header_used = {}
        for chunk in lines_with_metadata:
            metadata = chunk["metadata"]
            headers_html = ""
            headers_markdown = ""
            chunk_raw_text = ""
            for k, v in metadata.items():
                current_level = heading_levels.get(k, 10)
                header = v.get("data")
                header_html = v.get("html")
                header_markdown = v.get("markdown")
                if header not in header_used:
                    header_used[header] = 1
                    headers_html += header_html
                    headers_markdown += header_markdown + "\n\n"
                    chunk_raw_text += header + "\n\n"
            metadata["html"] = headers_html + chunk["html"]
            metadata["markdown"] = headers_markdown + "\n\n" + chunk["markdown"]
            metadata["chunk_raw_text"] = chunk_raw_text + "\n\n" +  chunk["content"]
            documents.append(
                Document(page_content=metadata["chunk_raw_text"], metadata=metadata)
            )

        # TODO: 进行语义分割
        if use_semantic:
            documents = self.semantic_chunking(documents[:])

        # TODO: 根据一级标题拆分chunk 
        # 如果是header标签比较多的，适合用这种形式
        if use_header:  
            documents = self.header_chunking(documents[:])

        # documents是粒度小的文档，用于构建索引；group_documents是粒度大的文档，用于分块QA生成
        return documents
    
    # def page_chunking(self,documents):
    #     # 第X页；第X页，共X页；1/X；第1/X页
    #     reg = re.compile(r"([第]?\w+[/]\w+[页]?)|([第][ ]?\w+[ ]?[页])")
    #     raw_text = ""
    #     for doc in documents:
    #         raw_text += doc.metadata['chunk_raw_text']
        
    #     mtchs = reg.finditer(raw_text)
        
        
    def cosine_distance(self, texts):
        # 计算文章chunks间的余弦距离
        embs = embed_texts_api(texts)
        cosine_dist = 1 - (np.array(embs) @ np.array(embs).T)
        return np.diagonal(cosine_dist, offset=1)

    def semantic_rechunking(
        self, documents: List[Document], indices_above_thresh: List[int]
    ) -> List[Document]:
        if not indices_above_thresh:
            return documents
        documents_new = []
        start_index = 0
        for idx in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = idx
            group = documents[start_index : end_index + 1]
            if len(group) > 1:
                doc = self.merge_chunk_group(group)
            else:
                doc = group[0]
            documents_new.append(doc)
            start_index = idx + 1

        # this last group if it remains
        if start_index < len(documents):
            group = documents[start_index:]
            if len(group) > 1:
                doc = self.merge_chunk_group(group)
            else:
                doc = group[0]
            documents_new.append(doc)

        return documents_new

    def semantic_chunking(
        self,
        documents: List[Document],
        threshold: float = 0.3,
        breakpoint_percentile_threshold: int = 50,
    ) -> List[Document]:
        chunks_raw_texts = []
        for doc in documents:
            chunks_raw_texts.append(doc.page_content)
        dists = self.cosine_distance(chunks_raw_texts)
        if breakpoint_percentile_threshold:
            threshold = np.percentile(dists, breakpoint_percentile_threshold)
        indices_above_thresh = np.where(dists >= threshold)[0].tolist()
        documents = self.semantic_rechunking(documents, indices_above_thresh)
        return documents

    def merge_chunk_group(
        self, chunk_group: List[Document], sub_chunk_size: int = SENTENCE_SIZE
    ) -> List[Document]:
        # TODO: chunks组合过长时，拆分子chunks
        docs = []
        if len(chunk_group) == 1:
            cur_chunk = chunk_group[0]
            chunk_group_text = cur_chunk.page_content
            chunk_group_metadata = cur_chunk.metadata.copy()
            # TODO:强制处理，如果超过最长限制，直接截取
            if len(chunk_group_text) >= self.MILVUS_CHUNK_MAX_LENGTH:
                chunk_group_text = chunk_group_text[: self.MILVUS_CHUNK_MAX_LENGTH - 1]
                chunk_group_metadata["chunk_raw_text"] = chunk_group_text
                chunk_group[0].page_content = chunk_group_text
                chunk_group[0].metadata = chunk_group_metadata
            return chunk_group
        chunk_group_text_remove_puncs = ""  # 移除标点符号后的文字 
        chunk_group_text, chunk_group_markdown, chunk_group_html = "", "", ""
        chunk_group_metadata = chunk_group[0].metadata.copy()

        for i, cur_chunk in enumerate(chunk_group):
            chunk_group_text += (
                cur_chunk.page_content + "\n\n" if cur_chunk.page_content else ""
            )
            chunk_group_text_remove_puncs += (
                remove_punctuation(cur_chunk.page_content) + "\n\n"
                if cur_chunk.page_content
                else ""
            )
            chunk_group_markdown += (
                cur_chunk.metadata.get("markdown", "") + "\n\n"
                if cur_chunk.metadata.get("markdown", "")
                else ""
            )
            chunk_group_html += (
                cur_chunk.metadata.get("html", "")
                if cur_chunk.metadata.get("html", "")
                else ""
            )
            if len(chunk_group_text_remove_puncs) >= sub_chunk_size:
                chunk_group_metadata["html"] = chunk_group_html
                chunk_group_metadata["markdown"] = chunk_group_markdown
                if len(chunk_group_text) >= self.MILVUS_CHUNK_MAX_LENGTH: # 强制处理
                    # TODO: 强制处理貌似没有起作用,milvus统计字符的方式不是简单的字符数
                    chunk_group_text = chunk_group_text[: self.MILVUS_CHUNK_MAX_LENGTH - 1]
                chunk_group_metadata["chunk_raw_text"] = chunk_group_text
                docs.append(
                    Document(
                        page_content=chunk_group_text, metadata=chunk_group_metadata
                    )
                )
                chunk_group_text, chunk_group_markdown, chunk_group_html = "", "", ""
                chunk_group_text_remove_puncs = ""
                chunk_group_metadata = chunk_group[0].metadata.copy()

        if chunk_group_text:
            if len(chunk_group_text) >= self.MILVUS_CHUNK_MAX_LENGTH: # 强制处理
                chunk_group_text = chunk_group_text[: self.MILVUS_CHUNK_MAX_LENGTH - 1]
            chunk_group_metadata["html"] = chunk_group_html
            chunk_group_metadata["chunk_raw_text"] = chunk_group_text
            chunk_group_metadata["markdown"] = chunk_group_markdown
            docs.append(
                Document(page_content=chunk_group_text, metadata=chunk_group_metadata)
            )
        return docs  

    def header_chunking(self, documents: List[Document]) -> List[Document]:
        # TODO: 根据一级标题拆分chunk
        if len(documents) == 1:
            # page_content = documents[0].page_content
            # if len(page_content) > chinese_textsplitter.sentence_size:
            #     return [Document(
            #         page_content=text) for text in chinese_textsplitter.split_text1(page_content)]
            return documents
        documents_new = []
        start, end = 0, 1

        while end < len(documents):
            doc = documents[end]
            metadata = doc.metadata
            h1 = metadata.get(HEADING1)
            h2 = metadata.get(HEADING2)

            if h1 and not h2:
                chunk_merged = self.merge_chunk_group(documents[start:end])
                documents_new.extend(chunk_merged)
                start = end
            end += 1

        if start < end:
            documents_new.extend(self.merge_chunk_group(documents[start:end]))
        return documents_new


document_header_splittor = DocumentHeaderTextSplitter()
