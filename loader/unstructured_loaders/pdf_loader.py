# -*- coding: utf-8 -*-
"""
  @CreateTime	:  2023/12/12 13:45:33
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
"""
import os
import sys

sys.path.append("./")

import uuid
import re
import json
import base64
import logging
import collections
from copy import deepcopy
from typing import List, Tuple, Dict, Optional, Any, Union, IO, AnyStr
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count,Manager
from time import perf_counter

from pprint import pprint

# import msgpack
from tqdm import tqdm
import fitz
import cv2
import pandas as pd
import numpy as np
from scipy import stats
from treelib import Tree, Node
from bs4 import BeautifulSoup

from pdf2docx import Converter
from pdf2docx.page.Pages import Pages
# from rapidocr_onnxruntime import RapidOCR
from langchain.docstore.document import Document

from loader.unstructured_loaders.constants import *
from loader.unstructured_loaders.loader import FileLoader

from utils.common import convert_base64_to_buffer, upload_file, timeit
from utils.string_util import normalize
from configs.apollo_config import logger

# ocr = RapidOCR()



class ConversionException(Exception):
    pass


class MakedocxException(ConversionException):
    pass


class CustomConverter(Converter):
    from utils.common import timeit

    def __init__(
        self, pdf_file: str = None, file_stream: BytesIO = None, password: str = None
    ):
        self.filename_pdf = pdf_file
        self.password = str(password or "")
        self._fitz_doc = None
        if pdf_file is not None and os.path.exists(pdf_file):
            self._fitz_doc = fitz.Document(pdf_file)
        if file_stream is not None:
            self._fitz_doc = fitz.Document(stream=file_stream, filetype="pdf")
        # initialize empty pages container
        self._pages = Pages()
        

    def _convert_with_multi_processing(
        self, docx_filename, start: int, end: int, **kwargs
    ):
        """Parse and create pages based on page indexes with multi-processing
        Reference:

            https://pymupdf.readthedocs.io/en/latest/faq.html#multiprocessing
        """
        # make vectors of arguments for the processes
        cpu = (
            min(kwargs["cpu_count"], cpu_count())
            if kwargs["cpu_count"]
            else cpu_count()
        )
        cpu = min(cpu,4)
        prefix = "pages"
        vectors = [
            (
                i,
                cpu,
                start,
                end,
                docx_filename,
                self.password,
                kwargs,
                f"{prefix}-{i}.json",
            )
            for i in range(cpu)
        ]
        # start parsing processes
        pool = Pool()
        pool.map(self._parse_pages_per_cpu, vectors, 1)

        # restore parsed page data
        for i in range(cpu):
            filename = f"{prefix}-{i}.json"
            if not os.path.exists(filename):
                continue
            self.deserialize(filename)
            os.remove(filename)
            
    def store(self):
        '''Store parsed pages in dict format.'''
        return {
            # 'filename': os.path.basename(self.filename_pdf),
            'page_cnt': len(self._pages), # count of all pages
            'pages'   : [page.store() for page in self._pages if page.finalized], # parsed pages only
        }
    
    # def serialize(self, filename: str):
    #     """Write parsed pages to specified JSON file with mspack"""
    #     with open(filename, 'wb') as f:
    #         msgpack.dump(self.store(), f) # 存储数据
    
    # def deserialize(self, filename: str):
    #     '''Load parsed pages from specified JSON file.'''
    #     with open(filename, 'rb') as f:
    #         data = msgpack.load(f, use_list=False, encoding='utf-8') # 读取数据
    #     self.restore(data)

            
    @staticmethod
    def _parse_pages_per_cpu(vector):
        '''Render a page range of a document.
        
        Args:
            vector (list): A list containing required parameters.
                * 0  : segment number for current process                
                * 1  : count of CPUs
                * 2,3: whole pages range to process
                * 4  : pdf filename or stream
                * 5  : password for encrypted pdf
                * 6  : configuration parameters
                * 7  : json filename storing parsed results
        '''        
        # recreate the arguments
        idx, cpu, s, e, pdf_file, password, kwargs, json_filename = vector

        # open pdf to get page count: all pages are marked to parse temporarily 
        # since don't know which pages to parse for this moment
        if isinstance(pdf_file,str):
            cv = CustomConverter(pdf_file=pdf_file, password=password)
        else:
            cv = CustomConverter(file_stream=pdf_file, password=password)
        cv.load_pages()

        # the specified pages to process
        e = e or len(cv.fitz_doc)
        all_indexes = range(s, e)
        num_pages = len(all_indexes)

        # page segment processed by this cpu
        m = int(num_pages/cpu)
        n = num_pages % cpu
        seg_size = m + int(idx<n)
        seg_from = (m+1)*idx + min(n-idx, 0)
        seg_to = min(seg_from + seg_size, num_pages)
        page_indexes = [all_indexes[i] for i in range(seg_from, seg_to)]

        # now, mark the right pages
        for page in cv.pages: page.skip_parsing = True
        for i in page_indexes: 
            cv.pages[i].skip_parsing = False

        # parse pages and serialize data for further processing
        cv.parse_document(**kwargs) \
            .parse_pages(**kwargs) \
            .serialize(json_filename)
        cv.close()

class PDFLoader(FileLoader):
    pattern = r"丨(.*?)丨"  # use to extract image placeholder
    delimiter = "丨"

    def __init__(
        self,
        file_path: str = None,
        file_stream: BytesIO = None,
        use_tree: bool = False,
        use_upload_file: bool = True,
    ) -> None:
        super().__init__(file_path, file_stream)
        # # use to deduplicate images often in pdf transform from ppt
        self.table_images = collections.defaultdict(list)  
        self.block_images = collections.defaultdict(list)
        self.blocks, self.maybe_title = self.pdf2blocks()
        self.blocks2html(self.blocks[:],use_upload_file=use_upload_file, use_parrallel=True)

    def check_row_lines(self, spans, margin=5) -> bool:
        """y轴上的差很接近，基本就是一行"""
        if not spans:
            return False
        if len(spans) == 1:
            return True
        res = []
        first_bbox = spans[0]["bbox"]
        first_height = first_bbox[-1] - first_bbox[1]
        for line in spans[1:]:
            bbox = line["bbox"]
            height = bbox[-1] - bbox[1]
            res.append(abs(height - first_height) <= margin)
        return all(res)

    def merge_lines(self, block) -> Any:
        """将一个block中的若干行合并起来"""
        spans = block["lines"][0]["spans"]
        bbox = block["bbox"]
        if self.check_row_lines(spans):
            concat_text = ""
            for span in spans:
                concat_text += span["text"]
            concat_text = normalize(concat_text)
            new_lines = {
                "color": span["color"],
                "font": span["font"],
                "size": span["size"],
                "bbox": bbox,
                "text": concat_text,
            }
            block["lines"][0]["spans"] = [new_lines]
        return block

    def merge_spans(self, spans, bbox) -> Any:
        """将一个line里面的spans行合并起来"""
        concat_text = ""
        # if self.check_row_lines(spans):
        for span in spans:
            concat_text += span["text"]
        concat_text = normalize(concat_text)
        merge_spans = {
            "color": span["color"],
            "font": span["font"],
            "size": span["size"],
            "bbox": bbox,
            "text": concat_text,
        }
        return merge_spans

    @timeit
    def rows2table(self, rows, restore_merge_cells=False):
        """rows转为tables，某个cell中可能有图片和文字的混合输入
        bid: 当前属于第几个block
        rows: 用于转换为表格的行数据
        restore_merge_cells: 是否恢复合并单元格内容，默认恢复
        """
        r = len(rows)
        c = len(rows[0]["cells"])
        df = [["" for i in range(c)] for j in range(r)]
        image_num = 0
        try:
            for i, row in enumerate(rows):
                if not row:
                    continue
                for j, cell in enumerate(row["cells"]):
                    if not cell:
                        continue
                    cell_blocks = cell["blocks"]
                    if not cell_blocks:
                        df[i][j] = ""
                        continue
                    # 一个cell可能会分行显示，需要拼接
                    # TODO:合并单元格 merged_cells = (2,1) 表示单元是2行，1列,如果是(1,3) 表示是1行，3列
                    merged_cell = cell.get("merged_cells", (1, 1))
                    if restore_merge_cells:
                        if merged_cell[-1] > 1:
                            # 合并列的单元格赋值
                            for k in range(1, merged_cell[-1]):
                                cell["merged_cells"] = (1, 1)
                                row["cells"][k] = deepcopy(cell)
                                rows[i]["cells"][j]["merged_cells"] = (1, 1)
                        if merged_cell[0] > 1:
                            # 合并行的单元格赋值
                            for k in range(1, merged_cell[0]):
                                cell["merged_cells"] = (1, 1)
                                rows[i + k]["cells"][j] = deepcopy(cell)
                                rows[i]["cells"][j]["merged_cells"] = (1, 1)
                    cell_text = ""
                    for cell_block in cell_blocks:
                        lines = cell_block.get("lines", [])
                        for line in lines:
                            spans = line.get("spans", [])
                            if not spans:
                                rows = line.get("rows", [])
                                for row in rows:
                                    print("当前的rows:", row)
                            span_text = ""  # html样式
                            # span_md = ""  # markdown样式
                            for l, span in enumerate(spans):
                                # cell内有图片
                                image = span.get("image")
                                if image:
                                    bbox = span.get("bbox")
                                    w, h = self.get_bbox_width_height(bbox)
                                    width = span.get("width")
                                    height = span.get("height")
                                    image_tag = (
                                        f"{self.delimiter}{image}${width}${height}{self.delimiter}"
                                    )
                                    span_text += image_tag
                                    if len(spans) > 1:
                                        span_text += "<br>"
                                else:
                                    span_text += span.get("text", "")
                            cell_text += span_text  # + "<br>"
                            if len(lines) > 1:
                                cell_text += "<br>"
                        # TODO: 表格单元格内还有表格
                        rows = cell_block.get("rows", [])
                        for row in rows:
                            if not row:
                                continue
                            cells = row.get("cells",[])
                            for cell in cells:
                                if not cell:
                                    continue
                                blocks = cell.get("blocks",[])
                                for blk in blocks:
                                    if not blk:
                                        continue
                                    lines = blk.get("lines", [])
                                    for line in lines:
                                        if not line:
                                            continue
                                        span_text = ""
                                        spans = line.get("spans", [])
                                        for l,span in enumerate(spans):
                                            span_text += span.get("text", "")
                                            if len(spans) > 1:
                                                span_text += "<br>"
                                        cell_text += span_text
                                    if len(lines) > 1:
                                        cell_text += "<br>"
                    df[i][j] = cell_text
        except Exception as e:
            print(e)
            print(f"{i},{j},当前的rows:", row)

        if len(df) <= 1:
            return pd.DataFrame(columns=df[0]), None

        columns = [c.strip().replace("<br>", "") for c in df[0]]
        has_column_header = len([c for c in columns if c]) > len(
            [c for c in columns if not c]
        )
        # 非数字开头
        if columns[0].isdigit():
            has_column_header = False
        if columns[0] and all(columns[1:]) is False:
            has_column_header = True
        if has_column_header:
            return (
                pd.DataFrame(index=None).from_records(df[1:], columns=df[0]),
                has_column_header,
            )
        return pd.DataFrame(index=None).from_records(df), has_column_header

    def merge_double_page_spread(
        self, table1: pd.DataFrame = None, table2: pd.DataFrame = None
    ):
        """合并跨页表格
        连续两页的表格，第一个页有表头，第二页无表头，合并上一页的表尾和当前页的表头
        注意：页眉页脚需要剔除掉，记得有单独的逻辑剔除
        """
        t1l = table1.iloc[-1, :].tolist()
        t2l = table2.columns.tolist()
        if not all(t2l):
            merge_line = ["<br>".join([str(l1), str(l2)]) for l1, l2 in zip(t1l, t2l)]
            table1.iloc[-1, :] = merge_line
        table2.columns = table1.columns
        return pd.concat([table1, table2]).reset_index(drop=True)

    @timeit
    def extract_blocks(self) -> List:
        blocks = []
        # convertor = Converter(file_path)
        convertor = CustomConverter(
            pdf_file=self.file_path, file_stream=self.file_stream
        )
        # default_settings = convertor.default_settings
        # convertor.parse(**default_settings)
        file_obj = self.file_path
        if self.file_stream:
            file_obj = self.file_stream
        convertor.convert(docx_filename=file_obj, multi_processing=True)
        if self.file_stream:
            del self.file_stream
        for page in convertor._pages:
            for section in page.sections:
                # section_store = section.store()
                blks = section.store()["columns"][0]["blocks"]
                # 添加page页面的section属性 方便计算每个block在页面的位置
                x0, x1, y0, y1 = (
                    section.bbox.x0,
                    section.bbox.x1,
                    section.bbox.y0,
                    section.bbox.y1,
                )
                for blk in blks:
                    blk.setdefault("section_bbox", (x0, y0, x1, y1))
                blocks.extend(blks)
        return blocks

    def get_bbox_width_height(self, bbox) -> tuple():
        """获取bbox的长和高"""
        x0, y0, x1, y1 = bbox
        return x1 - x0, y1 - y0

    def get_title_from_first_page(self, blocks, mode, n=2, min_len=4) -> Optional:
        """
        人为规则判断是否是标题，前三页中文本行大于文档常用字体的2倍大小，字数长度大于4的认为可能是标题
        TODO:位置是否居中???
        """
        for block in blocks:
            style = block["style"]
            if style in ["table", "image"]:
                continue
            height = block["height"]
            if height >= n * mode and len(block["data"]) >= min_len:
                return block["data"]

    def re_match(self, text):
        """
        正则，用于删除页眉页脚
        """
        reg = re.compile(r"[第共][ ]?[0-9]+[ ]?[页]")
        return reg.search(text)

    def replace_page_num(self, text):
        """统一替换多少页"""
        return re.sub(r"([第][ ]?)[0-9]+([ ]?[页])", r"\g<1>{}\g<2>", text)

    def validate_one_line_table(self, table, bbox=None, section_bbox=None):
        """校验一行的表格合法性；同时包括排除页眉页脚内容
        位于行首或行尾
        """

        def page_header(bbox, section_bbox, thres=3):
            """页眉 左上角的点x,y(x0,y0)轴和页面相同，右上角的点x,y(x1,y0)轴和页面相同"""
            x0, y0, x1, y1 = bbox
            sx0, sy0, sx1, sy1 = section_bbox
            if abs(sx0 - x0 + sy0 - y0 <= thres) and abs(sx1 - x1 + sy0 - y0 <= thres):
                return True
            return False

        def page_footer(bbox, section_bbox, thres=3):
            """页脚 左下角的点x,y(x0,y1)轴和页面的相同，右下角的点x,y(x1,y1)轴和页面相同"""
            x0, y0, x1, y1 = bbox
            sx0, sy0, sx1, sy1 = section_bbox
            if abs(sx0 - x0 + sy1 - y1 <= thres) and abs(sx1 - x1 + sy1 - y1 <= thres):
                return True
            return False

        text_line = self._join_columns(table.columns.tolist()).replace(" ", "")
        if (
            self.re_match(text_line)
            or page_header(bbox=bbox, section_bbox=section_bbox)
            or page_footer(bbox=bbox, section_bbox=section_bbox)
        ):
            text_line = self.replace_page_num(text_line)
            if (
                text_line in self.maybe_header_footer
            ):  # 如果存在于单行表格中，基本就是页眉
                self.maybe_header_footer[text_line] += 1
                return
            # 如果是因为解析分列出现问题，将页眉拆分为多个列，也需要判别
            if any(
                [
                    text_line in item
                    for item, freq in self.maybe_header_footer.items()
                    if freq > 1
                ]
            ):
                return
            self.maybe_header_footer[text_line] += 1
            # return
        return text_line

    def _join_columns(self, columns, sep=" "):
        """合并列"""
        res = []
        for column in columns:
            column = str(column).strip()
            if "<img" in column:
                column = "image"  # placeholder for image, better to use base64 image
            res.append(column)
        return sep.join(res)

    def remove_header_footer(self, blocks):
        """TODO:在合并blocks后，二次剔除页眉页脚
        合并blocks时，统计了header footer的数量，最高频的2个作为页眉页脚

        可能存在的问题:1.布局分析正确,页眉页脚完整
            2.布局分析错误，页眉页脚被拆开
        """
        blocks_flt = []
        sorted_header_footer = sorted(
            self.maybe_header_footer.items(), key=lambda item: item[1], reverse=True
        )
        most_common_header_footer = [
            item[0] for item in sorted_header_footer[:2] if item[1] > 1
        ]
        if not most_common_header_footer:
            return blocks
        for i, block in enumerate(blocks):
            d = block["data"]
            if not isinstance(d, str):
                blocks_flt.append(block)
                continue
            d = self.replace_page_num(d)
            if any([mc for mc in most_common_header_footer if d in mc]):
                continue
            blocks_flt.append(block)
        return blocks_flt

    def fix_header_footer(self, table) -> pd.DataFrame:
        """修正表格的页眉页脚bug case，因为表格识别错误导致的页眉页脚误判 以《收入核算操作指引》为例"""
        try:
            cols = []  # 需要去重
            for column in table.columns.tolist():
                # 去除重复且长度大于1的列
                column = str(column).strip()
                if len(column) > 1 and column in cols:
                    continue
                cols.append(column)
            row_first_text = self._join_columns(cols).replace(" ", "")
            row_first_line = self.replace_page_num(row_first_text)
            if row_first_line in self.maybe_header_footer or self.re_match(
                row_first_line
            ):
                if len(table) > 1:
                    table = (
                        table.iloc[1:, :] if len(table) > 1 else pd.DataFrame()
                    )  # 删除行名
                    table.columns = table.iloc[0, :].tolist()
                else:
                    table = pd.DataFrame(columns=table.columns.tolist())
                return table

            row_last = []  # 需要去重
            for column in table.iloc[-1, :].tolist():
                column = str(column).strip()
                if len(column) > 1 and column in row_last:
                    row_last.append(column)
            row_last_text = self._join_columns(row_last).replace(" ", "")
            row_last_line = self.replace_page_num(row_last_text)
            if row_last_line in self.maybe_header_footer or self.re_match(
                row_last_line
            ):
                table = table.iloc[:-1, :]
                return table
        except Exception as e:
            logger.error(e)
        return table

    @timeit
    def pdf2blocks(self) -> Tuple[List, int, Optional[str]]:
        """blocks -> lines/table -> spans -> text/image"""
        blocks = self.extract_blocks()
        merge_blocks = []
        for i, block in tqdm(enumerate(blocks)):
            bbox = block["bbox"]
            width, height = self.get_bbox_width_height(bbox=bbox)
            block["width"] = width
            block["height"] = height
            lines = block.get("lines")
            rows = block.get("rows")
            if not lines and not rows:
                continue

            # 表格处理
            if rows:
                table, has_header = self.rows2table(rows,restore_merge_cells=False)
                if 1 <= len(table):  # 删除因表格识别错误带入的header or footer
                    table = self.fix_header_footer(table)
                # TODO:空表格
                if table.empty:
                    f = self.validate_one_line_table(table, bbox, block["section_bbox"])
                    if not f:
                        continue
                    else:
                        # 将只有表头的表格转为字符串
                        # cblock = deepcopy(block)
                        # cblock["style"] = NORMAL
                        # cblock["data"] = f
                        # merge_blocks.append(cblock)
                        
                        # 尝试保持表格
                        block['style'] = "table"
                        block['data'] = table
                        merge_blocks.append(block)
                        continue
                # 跨页表格
                prev_style, prev_block = None, None
                if i > 0:
                    prev_block = merge_blocks[-1]
                    prev_style = prev_block["style"]

                if (
                    prev_block
                    and prev_block["style"] == "table"
                    and not prev_block['data'].empty
                    and (len(prev_block["data"].columns) == len(table.columns))
                    and not table.empty
                ):
                    merge_blocks[-1]["data"] = self.merge_double_page_spread(
                        prev_block["data"], table
                    )
                    continue

                # 删除空列，空行
                if has_header or (prev_style is not None and prev_style != "table"):
                    block["style"] = "table"
                    block["data"] = (
                        table.replace("", np.nan, regex=True)
                        .dropna(axis=1, how="all")
                        .fillna("")
                    )
                    block["uuid"] = uuid.uuid1().hex
                    block["has_header"] = has_header
                    merge_blocks.append(block)
                    continue

                block["style"] = "table"
                block["data"] = (
                    table.replace("", np.nan, regex=True)
                    .dropna(axis=1, how="all")
                    .fillna("")
                )
                block["uuid"] = uuid.uuid1().hex
                block["has_header"] = has_header
                merge_blocks.append(block)
                continue

            for j, line in enumerate(lines):
                spans = line.get("spans")
                if not spans:
                    continue
                bbox = line.get("bbox")
                contains = [span.get("image", False) for span in spans]
                if not any(contains):
                    merge_spans = self.merge_spans(spans, bbox=bbox)
                    width, height = self.get_bbox_width_height(bbox=bbox)
                    span_text = normalize(merge_spans["text"])
                    style = self.header_recoginze(span_text)
                    cblock = deepcopy(block)
                    cblock["data"] = span_text
                    cblock["style"] = style
                    cblock["bbox"] = bbox
                    cblock["width"] = width
                    cblock["height"] = height
                    cblock["font"] = merge_spans["font"]
                    cblock["size"] = merge_spans["size"]
                    cblock["color"] = merge_spans["color"]
                    merge_blocks.append(cblock)
                else:
                    for k, span in enumerate(spans):
                        span_bbox, color, size, font, span_text = (
                            span["bbox"],
                            span.get("color", 0),
                            span.get("size"),
                            span.get("font"),
                            span.get("text"),
                        )
                        image = span.get("image", "")
                        if image:
                            cblock = deepcopy(block)
                            cblock["uuid"] = uuid.uuid1().hex
                            cblock["style"] = "image"
                            cblock["data"] = image
                            cblock["bbox"] = span_bbox
                            ocr_text = self.image_recog(image)
                            cblock["text"] = ocr_text
                            del image
                            # cblock["text"] = ""
                            merge_blocks.append(cblock)
                            continue

                        cblock = deepcopy(block)
                        style = span.get(["style"], NORMAL)
                        if k == 0:
                            span_norm_text = normalize(span_text)
                            style = self.header_recoginze(span_norm_text)
                        cblock.update(span)
                        cblock["style"] = style
                        cblock["data"] = span_text
                        merge_blocks.append(cblock)
        # merge_blocks = self.remove_header_footer(merge_blocks)
        # 获取文件首页标题
        try:
            mode = None
            line_heights = [
                int(block["height"])
                for block in merge_blocks
                if block["style"] not in ["image", "table"]
            ]
            mode = stats.mode(line_heights)[0][0]
            mb_title = self.get_title_from_first_page(
                blocks=merge_blocks[:3], mode=mode
            )
        except Exception as e:
            logger.error(e)
        # 如果没有mb_title就用文件名称
        file_name = self._validate_filename()
        if file_name:
            mb_title = file_name
        return merge_blocks, mb_title

    def build_tree(self, file_path, blocks, title) -> Tree:
        prefix = file_path.rsplit(".")[0]
        pkl_path = prefix + ".pkl"
        if os.path.exists(pkl_path):
            logger.info("Loading tree pickle file which is already saved!")
            return self.load(pkl_path)
        tree = Tree()
        # blocks,mode,maybe_title = self.pdf2blocks(file_path=file_path)
        root = tree.create_node(
            tag="root",
            identifier="root",
            data={"type": "text", "style": "Title", "data": title, "name": None},
        )
        self.build_document_tree(blocks=blocks, parent=root, tree=tree)
        self.persist(tree, save_path=pkl_path)
        return tree

    def build_document_tree(self, blocks, parent, tree=None) -> None:
        """构建文档tree"""
        for i, block in enumerate(blocks):
            style = block["style"]
            if style == "table":
                uid = block["uuid"]
                tag = f"table_{uid}"
            elif style == "image":
                uid = block["uuid"]
                tag = f"image_{uid}"
            else:
                tag = block["text"]
            node = Node(tag=tag, identifier=tag, data=block)
            if style.startswith("Heading"):
                h_level = int(heading_levels[style])
                parent_h = parent.data["style"]
                parent_h_level = int(heading_levels[parent_h])
                if parent_h_level < h_level:  # 添加子节点
                    new_parent = parent
                else:
                    new_parent = None
                    while tree.parent(parent.identifier):
                        parent = tree.parent(parent.identifier)
                        new_parent_h = parent.data["style"]
                        new_parent_h_level = int(heading_levels[new_parent_h])
                        if new_parent_h_level < h_level:
                            new_parent = parent
                            break
                if not tree.get_node(tag):
                    tree.add_node(node, parent=new_parent.identifier)
                    self.build_document_tree(blocks[i + 1 :][:], parent=node, tree=tree)
            else:
                if not tree.get_node(tag):
                    tree.add_node(node, parent=parent.identifier)
                    self.build_document_tree(
                        blocks[i + 1 :][:], parent=parent, tree=tree
                    )

    def query_content_by_chapter_section(self, query):
        """获取问题中对应的章节内容"""
        chapter_idx, section_idx, subsection_idx = self.extract_chapter_section(query)
        if not chapter_idx:
            return

        def traverse(chapter_idx, section_idx, subsection_idx):
            childs = self.tree.children("root")
            if chapter_idx is not None and section_idx is None:
                return childs[chapter_idx]
            if (
                chapter_idx is not None
                and section_idx is not None
                and subsection_idx is None
            ):
                chapter = childs[chapter_idx]
                sections = self.tree.children(chapter.identifier)
                return sections[section_idx]
            if (
                chapter_idx is not None
                and section_idx is not None
                and subsection_idx is not None
            ):
                chapter = childs[chapter_idx]
                sections = self.tree.children(chapter.identifier)
                section = sections[section_idx]
                subsections = self.tree.children(section.identifier)
                return subsections[subsection_idx]

        return traverse(chapter_idx, section_idx, subsection_idx)

    def blocks2html(self, blocks,use_upload_file: bool = True, use_parrallel: bool = False):
        """将blocks转化为html,同时支持markdown格式的转换"""
        prefix = """
        <!DOCTYPE html>
        <div id="page0">\n"""
        suffix = """\n</div>"""

        def restore_table_images(blocks):
            """将表格单元格中的图片批量并行上传 多线程/多进程"""

            def restore_cell_image(i, j, k, b64img,width, height, assert_url):
                """替换单个单元格中的图片占位符
                i: block id
                j: dataframe的row idx
                k: dataframe的column idx
                b64img: 图片base64编码
                assert_url: 图片上传后的url
                """                    
                
                def replace_img(content,b64img,width,height,assert_url):
                    # 替换文本中的base64image
                    content = content.replace(f"{b64img}","b64img")
                    pat = f"丨b64img${width}${height}丨"
                    return content.replace(pat,assert_url if assert_url else "")
                columns = blocks[i]['data'].columns.tolist()
                df = blocks[i]['data'].to_numpy().tolist()
                if not df and not columns:
                    return blocks
                
                if j == -1: # 表头有图片
                    column_name = columns[k]
                    columns[k] = self.text2html(text=replace_img(content=column_name,b64img=b64img,width=width,height=height,assert_url=assert_url),
                                                style="image",
                                                width=width,
                                                height=height
                                                )
                else:
                    df[j][k]= self.text2html(
                        text=replace_img(content=df[j][k],b64img=b64img,width=width,height=height,assert_url=assert_url),
                        style="image",
                        width=width,
                        height=height
                    )
                
                if columns and not df:
                    df = pd.DataFrame(columns=columns)
                else:
                    df = pd.DataFrame(df)   
                    df.columns = columns
                blocks[i]["data"] = df
                    
                return blocks

            # 遍历所有表格中的图片
            for i, block in enumerate(blocks):
                style = block.get("style")
                if style != "table":
                    continue
                df = block.get("data")
                
                # if df.empty: # 有很多表格只有表头是empty dataframe,不需要限制
                #     continue

                # TODO:存在列名中包含图片的情况，需要单独处理
                for m,column_name in enumerate(df.columns.tolist()):
                    column_name = str(column_name)
                    if "丨" in column_name:
                        column_mtchs = re.finditer(self.pattern, column_name)
                        for mtch in column_mtchs:
                            start, mtch_cont = mtch.start(), mtch.group().replace(self.delimiter,"")
                            b64img, width, height = mtch_cont.split("$")
                            self.table_images[b64img].append(
                                (i,-1,m,start,width,height)
                            )
                
                for j in range(len(df)):
                    for k in range(len(df.columns)): 
                        cell_text = df.iloc[j, k]
                        if "丨" not in cell_text:
                            continue
                        matches = re.finditer(self.pattern, cell_text)
                        for mtch in matches:
                            start, mtch_cont = mtch.start(), mtch.group().replace(self.delimiter,"")
                            b64img, width, height = mtch_cont.split("$")
                            self.table_images[b64img].append(
                                # block_id,行,列,match_start,width,height,当j为-1时，表示是表头中有图片
                                (i, j, k, start, width, height)
                            )
            logger.info(
                f"uploading {len(self.table_images)} images of tables in parrallel..."
            )
            image_pairs = []
            image_dict = deepcopy(self.table_images)
            for i,(k,v) in enumerate(image_dict.items()):
                filename = uuid.uuid1().hex + ".jpg"
                # image_idx,文件名称,base64image,width,height
                image_pairs.append((i, filename, k) + v[0][4:])
            thread_results = self.upload_files_parallel(
                image_pairs=image_pairs, max_workers=8
            )
            for result in thread_results:
                idx, assert_url, width, height = result
                _, filename, b64img, width, height = image_pairs[idx]
                for i, j, k, _, _, _ in image_dict.get(b64img):
                    restore_cell_image(i, j, k, b64img,int(width), int(height), assert_url)
            return blocks
                    
        self.blocks = restore_table_images(blocks[:])
        
        for i, block in enumerate(self.blocks[:]):
            style = block["style"]
            if style in self.STYLE_MAP:
                text = block["data"]
                bold = block.get("bold")
                size = block.get("size")
                if style == "image": # 表格外的图片
                    width = block.get("width", 100)
                    height = block.get("height", 100)
                    file_name = block.get("filename", uuid.uuid1().hex + ".png")
                    block_html = ""
                    if use_upload_file:
                        self.block_images[text].append(
                            (i, file_name, width, height)
                        )
                        block_html = ""
                        block_markdown = ""
                else:
                    block_html = self.text2html(text, style, font_size=size)
                    block_markdown = self.text2markdown(text=text, style=style)
                if bold:
                    block_html = "<b>" + block_html + "</b>"
                    block_markdown = " **" + block_markdown + "**"
            elif style == "table":
                table = block["data"]
                table.style.set_table_styles(
                    [
                        {
                            "selector": "th,td",
                            "props": [
                                ("font-size", "12pt"),
                                ("border-style", "solid"),
                                ("border-width", "1px"),
                            ],
                        }
                    ]
                )
                if not table.empty:
                    block_html = table.to_html(
                        index=False, justify="left", classes="default-style", escape=False
                    )

                    block_markdown = table.to_markdown(index=False)
                else:
                    # 只有表头的表格转为多行字符串
                    columns = [column.replace("<br>","\n") for column in table.columns.tolist()]
                    block_html = self.text2html(
                        text="\n".join(columns),
                        style= NORMAL,
                        font_size="12pt"
                    )   
                    block_markdown = "\n".join(columns) + "\n\n"
                    self.blocks[i]['style'] = NORMAL
                    self.blocks[i]['data'] = "\n".join(columns)
            else:
                text = block["data"]
                style = "Normal"
                bold = block.get("bold")
                size = block.get("size")
                block_html = self.text2html(text, style, font_size=size)
                block_markdown = self.text2markdown(text=text, style=style)
                if bold:
                    block_html = "<b>" + block_html + "</b>"
                    block_markdown = " **" + block_markdown + "**"

            self.blocks[i]["html"] = block_html
            self.blocks[i]["markdown"] = block_markdown
        
        self.table_images = {}

        if use_parrallel:  # 重新赋值图片
            images_dict = deepcopy(self.block_images)
            block_images_pairs = [
                v[0][0:2] + (k,) + v[0][2:] for k, v in images_dict.items()
            ]
            logger.info(f"uploading {len(block_images_pairs)} images of blocks in parrallel...")

            thread_results = self.upload_files_parallel(image_pairs=block_images_pairs)
            for i, result in enumerate(thread_results):
                idx, assert_url, width, height = result
                if not assert_url:
                    self.blocks[idx]["html"] = ""
                block_html = self.text2html(
                    assert_url, style="image", width=width, height=height
                )
                # 上传的图片链接转markdown标签
                block_markdown = self.text2markdown(text=assert_url, style="image")
                self.blocks[idx]["html"] = block_html
                self.blocks[idx]["markdown"] = block_markdown
        self.block_images = {}


if __name__ == "__main__":
    abs_path = "/rainbow/zhangjunfeng/langchain-ChatGLM/knowledge_base/content/中国反洗钱报告.pdf"
    pdf_loader = PDFLoader(abs_path)
    # print(pdf_loader.tree)
