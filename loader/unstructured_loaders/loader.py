import os
import sys

sys.path.append("./")
import base64
from io import BytesIO
from typing import List

import cv2
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict
from treelib import Tree, Node
import cn2an
# from rapidocr_onnxruntime import RapidOCR

from loader.unstructured_loaders.constants import *
from utils.common import (
    pt2em,
    pt2px,
    convert_base64_to_buffer,
    upload_file,
    thread_parallel,
    ocr_api
)

# ocr = RapidOCR()


class FileLoader(object):
    STYLE_MAP = {
        "Heading 1": """<h{style}>{text}</h1>""",
        "Heading 2": """<h{style}>{text}</h2>""",
        "Heading 3": """<h{style}>{text}</h3>""",
        "Heading 4": """<h{style}>{text}</h4>""",
        "Heading 5": """<h{style}>{text}</h5>""",
        "Heading 6": """<h{style}>{text}</h6>""",
        "Title": """
            <head>
              <meta charset="utf-8">
              <title>{text}</title>
            </head>
        """,
        "Normal": """<p{style}>{text}</p>""",
        "image": """<img border="0" src="{text}" alt="Pulpit rock" width="{width}" height="{height}">""",
        # "table": 直接用pandas转html
    }

    MARKDOWN_STYPE_MAP = {
        "Heading 1": """# {text}""",
        "Heading 2": """## {text}""",
        "Heading 3": """### {text}""",
        "Heading 4": """#### {text}""",
        "Heading 5": """###### {text}""",
        "Heading 6": """####### {text}""",
        "image": "![]({text})",
        # "table": 直接用pandas转markdown
        "code": """```{language}
        {text}
        ```""",
    }

    # 表格固定样式
    HTML_STRING = """<html><head><title>HTML Pandas Dataframe with CSS</title></head><link rel="stylesheet" type="text/css" href="df_style.css"/><body>{table}</body></html>"""
    # html渲染固定开头
    HTML_PREFIX = """
<!DOCTYPE html>
<div id="page0">\n"""

    # html渲染固定结尾
    HTML_SUFFIX = """\n</div>"""

    # 文件名称的正则表达式
    # FILENAME_REG = TEST_FILENAMES

    def __init__(self, file_path: str = None, file_stream: BytesIO = None):
        self.file_path = file_path
        self.file_stream = file_stream
        self.maybe_header_footer = defaultdict(int)

    def _validate_filename(self):
        """文件名，过滤掉常见的测试文档名称"""
        file_name = self.file_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        # mtch = TEST_FILENAMES.search(file_name)
        # return file_name if mtch is None else None
        return file_name

    def image_recog(self, image):
        # img_array = np.frombuffer(base64.b64decode(image), np.uint8)
        # img_array = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        # result, _ = ocr(img_array)
        # ocr_text = ""
        # if result:
        #     ocr_result = [line[1] for line in result]
        #     ocr_text = "\n".join(ocr_result)
        # del img_array
        # return ocr_text
        return ocr_api(image)
    
    def image_recog_with_idx(self, idx, b64_data):
        """上传文件，并返回文件id"""
        return idx,self.image_recog(b64_data)

    def table2pd(self, table):
        """doc的table转dataframe"""
        df = [["" for i in range(len(table.columns))] for j in range(len(table.rows))]
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                if cell.text:
                    df[i][j] = cell.text
        return pd.DataFrame(df)

    def build_tree(self, file_path) -> Tree:
        raise NotImplementedError

    def extract_chapter_section(self, query) -> tuple():
        """简单获取问题中的章节索引 章 节 小节"""
        chapter_idx, section_idx, subsection_idx = None, None, None
        chapter = chapter_reg.search(query)
        if chapter:
            chapter_idx = chapter.group(1)
            if ZH_REG.search(chapter_idx):
                chapter_idx = cn2an.cn2an(chapter_idx)
        section = section_reg.search(query)
        if section:
            section_idx = section.group(1)
            if ZH_REG.search(section_idx):
                section_idx = cn2an.cn2an(section_idx)
        subsection = subsection_reg.search(query)
        if subsection:
            subsection_idx = subsection.group(1)
            if ZH_REG.search(subsection_idx):
                subsection_idx = cn2an.cn2an(subsection_idx)
        return chapter_idx, section_idx, subsection_idx

    def query_content_by_chapter_section(self, query):
        raise NotImplementedError

    def persist(self, tree, save_path):
        with open(save_path, "wb") as wf:
            pickle.dump(tree, wf)

    def load(self, save_path) -> Tree:
        with open(save_path, "rb") as rf:
            return pickle.load(rf)

    def text2html(
        self, text, style, width: int = None, height: int = None, font_size: int = None
    ):
        """将block的内容转换为html"""
        default_html_tag = self.STYLE_MAP.get(NORMAL)
        default_heading_level = heading_levels[NORMAL]
        heading_level = heading_levels.get(style, default_heading_level)
        html_tag = self.STYLE_MAP.get(style, default_html_tag)
        if style == "image":
            return html_tag.format(text=text, width=width, height=height)
        # 去除字体大小问题
        # if font_size:
        #     em = pt2em(font_size)
        #     if heading_level == default_heading_level:
        #         html_tag = html_tag.format(
        #             style=f""" style="font-size: {em}rem\"""", text=text
        #         )
        #     else:
        #         html_tag = html_tag.format(
        #             style=f"""{heading_level} style="font-size:{em}rem\"""", text=text
        #         )
        # else:
        #     if heading_level == default_heading_level:
        #         html_tag = html_tag.format(style="", text=text)
        #     else:
        #         html_tag = html_tag.format(style=f"{heading_level}", text=text)

        if heading_level == default_heading_level:
            html_tag = html_tag.format(style="", text=text)
        else:
            html_tag = html_tag.format(style=f"{heading_level}", text=text)
        return html_tag

    def text2markdown(self, text, style):
        """将block的内容转换为markdown
        后期可能要支持python,js代码等代码块
        """
        default_heading_level = heading_levels[NORMAL]
        heading_level = heading_levels.get(style, default_heading_level)
        markdown_tag = self.MARKDOWN_STYPE_MAP.get(style)
        if style == "image" or heading_level != default_heading_level:
            return markdown_tag.format(text=text)
        return text

    def header_recoginze(self, text):
        res = NORMAL
        h1_match = heading1_reg.search(text.strip())
        if h1_match:
            res = HEADING1
        h2_match = heading2_reg.search(text.strip())
        if h2_match:
            res = HEADING2
        h3_match = heading3_reg.search(text.strip())
        if h3_match:
            res = HEADING3
        h4_match = heading4_reg.search(text.strip())
        if h4_match:
            res = HEADING4
        h5_match = heading5_reg.search(text.strip())
        if h5_match:
            res = HEADING5
        h6_match = heading6_reg.search(text.strip())
        if h6_match:
            res = HEADING6
        return res

    def upload_file_with_idx(self, idx, filename, buffer_stream, width, height):
        """上传文件，并返回文件id"""
        assert_url = upload_file(filename, buffer_stream)
        return idx, assert_url, width, height

    def upload_files_parallel(self, image_pairs: List[tuple], max_workers=4):
        """多线程批量上传文件，并返回文件id列表
        image_pair: idx,filename,base64_image,width,height
        """
        args_list = []

        for i, filename, base64_image, width, height in image_pairs:
            buffer_stream = convert_base64_to_buffer(b64_data=base64_image)
            args_list.append((i, filename, buffer_stream, width, height))

        return thread_parallel(
            self.upload_file_with_idx, args_list=args_list, max_workers=max_workers
        )


if __name__ == "__main__":
    file_loader = FileLoader()
    q = "我想要第一章第二节的内容"
    cidx, sidx = file_loader.extract_chapter_section(q)
    print(cidx, sidx)
