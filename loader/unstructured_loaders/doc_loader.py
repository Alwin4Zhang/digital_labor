# -*- coding: utf-8 -*-

import os
import sys

sys.path.append("./")

import re
import uuid
import logging
from pprint import pprint
from typing import List, Tuple, Dict, Optional, Any, Iterator
from io import StringIO, BytesIO
import base64
from PIL import Image
import cv2
import docx
from docx import Document
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy import stats
from xml.etree import ElementTree
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph
from docx.shape import InlineShape
from docx.enum.style import WD_STYLE_TYPE, WD_BUILTIN_STYLE
from docx.enum.shape import WD_INLINE_SHAPE
from bs4 import BeautifulSoup

from treelib import Tree, Node
from rapidocr_onnxruntime import RapidOCR
from langchain.docstore.document import Document as LangChainDocument

from loader.unstructured_loaders.constants import *
from loader.unstructured_loaders.loader import FileLoader
from utils.common import (
    convert_base64_to_buffer,
    upload_file,
    pt2em,
    convert_file_type,
    convert_flowchart,
    save_bfile,
    crop_image,
    ocr_api
)
from utils.string_util import normalize
from configs.apollo_config import logger

# ocr = RapidOCR()
# logger = logging.Logger(__file__)

# WD_STYLE_TYPE
"""
CHARACTER 2
    Character style.
LIST  4
    List style.
PARAGRAPH 1
    Paragraph style.
TABLE 3
    Table style.
"""

tmp_files_path = os.path.join(os.path.dirname(__file__), "tmp_files")
if not os.path.exists(tmp_files_path):
    os.mkdir(tmp_files_path)


class DocLoader(FileLoader):

    def __init__(
        self, file_path: str = None, file_stream: BytesIO = None, use_tree: bool = False
    ) -> None:
        super().__init__(file_path, file_stream)
        self.images = {}
        self.blocks, self.maybe_title = self.doc2blocks()
        self.blocks2html()
        self.tree = None
        if use_tree:
            self.tree = self.build_tree(
                file_path=file_path, blocks=self.blocks, title=self.maybe_title
            )

    def iter_block_items(self, parent):
        parent_elm = None
        if isinstance(parent, _Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        elif isinstance(parent, _Row):
            parent_elm = parent._tr
        else:
            logger.error(f"Iter block items parent type is not right: {type(parent)}")
        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)
    
    def _iter_table_cells(self, table: Table) -> Iterator[_Cell]:
        # fork from https://github.com/python-openxml/python-docx/issues/1312
        """Generate each "visible" cell in `table`.
        Note that not all rows will necessarily have the same number of columns and
        a row can start in a column later than the first if there is a vertical merge.
        """
        # 预留方法，用于识别doc文档中的合并单元格
        for i, row in enumerate(table.rows):
            tr = row._tr
            for j,tc in enumerate(tr.tc_lst):
                # -- vMerge="continue" indicates a spanned cell in a vertical merge --
                if tc.vMerge == "continue":  # 纵向合并单元格
                    continue
                # -- --
                yield _Cell(tc, row),i,j

    def row2table(self, table,restore_merge_cells=True):
        """doc的table转dataframe"""
        df = [["" for i in range(len(table.columns))] for j in range(len(table.rows))]
        if not restore_merge_cells: # doc默认没有处理合并单元格，会将每个单元格赋值
            for i, row in enumerate(table.rows):
                for j, cell in enumerate(row.cells):
                    if cell.text:
                        df[i][j] = cell.text.replace("\n", "<br>")
        else:
            for cell,i,j in self._iter_table_cells(table):
                if cell.text:
                    df[i][j] = cell.text.replace("\n", "<br>")
        if len(df) <= 1:
            return pd.DataFrame(columns=df[0])
        return pd.DataFrame(index=None).from_records(df[1:], columns=df[0])

    def wmf2png(self, wmf_path):
        """将emf/wmf文件转为png"""
        """将emf/wmf文件转为png"""
        new_image_path = convert_flowchart(
            wmf_path, target_format="png", output_directory=tmp_files_path
        )

        return new_image_path

    def save_wmf(self, wmf_path):
        """保存wmf文件到oss"""
        new_image_path = self.wmf2png(wmf_path)
        if not new_image_path:
            return
        try:
            image_cv = crop_image(new_image_path)
            file_name = new_image_path.rsplit("/", 1)[-1]
            h, w, c = image_cv.shape
            image = cv2.imencode(".png", image_cv)[1]
            image_base64 = str(base64.b64encode(image))[2:-1]
            # 删除临时文件
            os.remove(wmf_path)
            os.remove(new_image_path)
            return new_image_path, image_base64, h, w
        except Exception as e:
            logger.error(f"save_wmf error: {e}")
            return

    def recognize_flowchat(self, tag="w:pict", soup=None, doc=None):
        """识别doc xml中的流程图,返回流程图保存的临时文件路径"""
        save_paths = []
        if not soup:
            return
        pict_elements = soup.find_all(tag)
        for elem in pict_elements:
            image_data = elem.find("v:imagedata")
            if not image_data:
                continue
            image_rid = image_data.get("r:id")
            if not image_rid:
                continue
            if image_rid not in doc.part.rels:
                continue
            rel = doc.part.rels[image_rid]
            image_stream = rel.target_part
            file_name = image_stream.filename
            content_type = image_stream.content_type
            uuid_str = uuid.uuid1().hex
            if file_name:
                n, ext = file_name.rsplit(".", 1)
                file_name = n + "_" + uuid_str + "." + ext
            else:
                file_name = uuid_str + ".emf"
            tmp_emf_save_path = os.path.join(tmp_files_path, file_name)
            is_saved = save_bfile(tmp_emf_save_path, image_stream._blob)
            if not is_saved:
                return
            save_paths.append(
                {
                    "uuid": uuid_str,
                    "filename": file_name,
                    "content_type": content_type,
                    "path": tmp_emf_save_path,
                }
            )
        return save_paths

    def image_to_block(
        self,
        index,
        uuid_str,
        image_base64,
        width,
        height,
        content_type,
        filename,
        name=None,
    ):
        """将图片转为block,同时ocr识别图片中的内容
        index: block index
        uuid_str: 图片的uuid
        image_base64: 图片的base64编码
        width: 图片的宽度
        height: 图片的高度
        content_type: 图片的content_type
        filename: 图片的filename
        name: 图片的名称，有时候原生对象中有图片名称，如果没有则使用filename
        """
        image_blk = {
            "index": index,
            "uuid": uuid_str,
            "type": "image",
            "style": "image",
            "data": image_base64,
            "name": name if name else filename,
            "text": "",
            "width": width,
            "height": height,
            "content_type": content_type,
            "filename": filename,
        }

        # img_array = np.frombuffer(base64.b64decode(image_base64), np.uint8)
        # img_array = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        # result, _ = ocr(img_array)
        # if result:
        #     ocr_result = [normalize(line[1]) for line in result]
        #     # TODO:识别图片中的内容
        #     ocr_text = "\n".join(ocr_result)
        #     image_blk["text"] = ocr_text
        ocr_text = ocr_api(image_base64)
        image_blk["text"] = ocr_text
        return image_blk

    def doc2blocks(self):
        doc = None
        if self.file_path is not None and os.path.exists(self.file_path):
            doc = Document(self.file_path)
        elif self.file_stream is not None:
            doc = Document(self.file_stream)
        blocks = []
        for i, block in enumerate(self.iter_block_items(doc)):
            if "_p" in block.__dict__:
                soup = BeautifulSoup(block._p.xml, "xml")
                if "w:pict" in block._p.xml:
                    emf_save_paths = self.recognize_flowchat(soup=soup, doc=doc)
                    for emf_tmp_path in emf_save_paths:
                        result = self.save_wmf(emf_tmp_path["path"])
                        if not result:
                            continue
                        _, image_base64, height, width = result
                        uuid_str = emf_tmp_path["uuid"]
                        content_type = "image/png"
                        file_name = emf_tmp_path["filename"].rsplit(".", 1)[0] + ".png"
                        image_blk = self.image_to_block(
                            index=i,
                            uuid_str=uuid_str,
                            image_base64=image_base64,
                            width=width,
                            height=height,
                            content_type=content_type,
                            filename=file_name,
                        )
                        blocks.append(image_blk)

                if "w:object" in block._p.xml:
                    emf_save_paths = self.recognize_flowchat(
                        tag="w:object", soup=soup, doc=doc
                    )
                    for emf_tmp_path in emf_save_paths:
                        result = self.save_wmf(emf_tmp_path["path"])
                        if not result:
                            continue
                        _, image_base64, height, width = result
                        uuid_str = emf_tmp_path["uuid"]
                        content_type = "image/png"
                        file_name = emf_tmp_path["filename"].rsplit(".", 1)[0] + ".png"
                        image_blk = self.image_to_block(
                            index=i,
                            uuid_str=uuid_str,
                            image_base64=image_base64,
                            width=width,
                            height=height,
                            content_type=content_type,
                            filename=file_name,
                        )
                        blocks.append(image_blk)
            # TODO: paragraph 对象中包含有toc style，说明当前段落是目录
            if "text" in str(block):
                bold_runs = []
                run_text = ""
                for k, run in enumerate(block.runs):
                    xmlstr = str(run.element.xml)
                    if not "pic:pic" in xmlstr:
                        if run.bold:
                            bold_runs.append(True)
                        else:
                            bold_runs.append(False)
                        run.text = whitespace_reg.sub(" ", run.text)
                        run_text += normalize(run.text)
                    if (
                        ("pic:pic" in xmlstr) or (k == len(block.runs) - 1)
                    ) and run_text:
                        style = self.header_recoginze(run_text)
                        if not block.style.name.startswith("Heading"):
                            if block.style.name.lower().startswith("toc"):
                            # or (
                            #     block.style.style_id.isnumeric()
                            #     and (int(block.style.style_id) == WD_STYLE_TYPE.LIST)
                            # ):  # 目录或者list，重新降级
                                block.style.name = "Normal"
                            else:
                                block.style.name = style
                        if run.style and run.style.name and run.style.name == "Strong":
                            bold_runs[-1] = True
                        if (
                            not all(bold_runs) and len(run_text.strip()) >= 20
                        ):  # TODO:降级，没加粗且文字超过一定个数,规则待商榷，更好的应该是占一行文本的比例
                            block.style.name = "Normal"
                        # TODO:如果header recog的header级别比block级别低，则降级；因为底层框架有时候会误识别header
                        if heading_levels.get(
                            block.style.name, 10
                        ) < heading_levels.get(style, 10):
                            block.style.name = style
                        d = {
                            "type": "text",
                            "style": block.style.name,
                            "size": (
                                block.style.font.size.pt
                                if block.style.font.size
                                else None
                            ),
                            "bold": all(bold_runs),
                            "data": run_text,
                            "name": None,
                        }
                        blocks.append(d)
                        run_text = ""

                    if "pic:pic" in xmlstr:
                        my_namespaces = dict(
                            [
                                node
                                for _, node in ElementTree.iterparse(
                                    StringIO(xmlstr), events=["start-ns"]
                                )
                            ]
                        )
                        root = ElementTree.fromstring(xmlstr)
                        for i, pic in enumerate(
                            root.findall(".//pic:pic", my_namespaces)
                        ):
                            # 当遇到图片时
                            cNvPr_elem = pic.find(
                                "pic:nvPicPr/pic:cNvPr", my_namespaces
                            )
                            name_attr = cNvPr_elem.get("name")
                            blip_elem = pic.find("pic:blipFill/a:blip", my_namespaces)
                            embed_attr = blip_elem.get(
                                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                            )
                            document_part = doc.part
                            if not embed_attr or document_part or document_part.related_parts:
                                continue
                            image_part = document_part.related_parts[embed_attr]
                            # TODO: base64 可能冗余
                            image_base64 = base64.b64encode(image_part._blob)
                            default_image_obj = image_part.image
                            content_type = default_image_obj.content_type
                            # 0.64是反向推出来的比例
                            width = default_image_obj.px_width * 0.64
                            height = default_image_obj.px_height * 0.64
                            file_name = default_image_obj.filename

                            image_d = self.image_to_block(
                                index=i,
                                uuid_str=uuid.uuid1().hex,
                                image_base64=image_base64,
                                width=width,
                                height=height,
                                content_type=content_type,
                                filename=file_name,
                                name=name_attr,
                            )
                            blocks.append(image_d)
            elif isinstance(block, Table):
                tb = self.row2table(block)
                if tb.empty:
                    continue
                blocks.append(
                    {
                        "uuid": uuid.uuid1().hex,
                        "type": "table",
                        "style": "table",
                        "data": tb,
                        "name": None,
                    }
                )

        try:
            mode = None
            line_heights = [
                int(block["size"])
                for block in blocks
                if block["type"] == "text" and block["size"]
            ]
            if line_heights:
                mode = stats.mode(line_heights)[0][0]
            mb_title = self.get_title_from_first_page(blocks=blocks[:3], mode=mode)
        except Exception as e:
            logger.error(e)
        # 如果没有mb_title就用文件名称
        file_name = self._validate_filename()
        if file_name:
            mb_title = file_name
        return blocks, mb_title

    def get_title_from_first_page(self, blocks, mode, n=2, min_len=4) -> Optional:
        """人为规则判断是否是标题，前三页中文本行大于文档常用字体的2倍大小，字数长度大于4的认为可能是标题"""
        if not mode:
            return
        for block in blocks:
            # height = block['size']
            height = block.get("size")
            if not height:
                continue
            if height >= n * mode and len(block["data"]) >= min_len:
                return block["data"]

    def build_tree(self, file_path, blocks, title) -> Tree:
        prefix = file_path.rsplit(".")[0]
        pkl_path = prefix + ".pkl"
        if os.path.exists(pkl_path):
            logger.info("Loading tree pickle file which is already saved!")
            return self.load(pkl_path)
        # blocks,mode,maybe_title = self.doc2blocks(file_path=file_path)
        tree = Tree()
        root = tree.create_node(
            tag="root",
            identifier="root",
            data={"type": "text", "style": "Title", "data": title, "name": None},
        )
        self.build_document_tree(blocks, root, tree=tree)
        self.persist(tree, save_path=pkl_path)
        return root

    def build_document_tree(self, blocks, parent, tree=None) -> None:
        """构建文档tree"""
        for i, block in enumerate(blocks):
            style = block["style"]
            type = block["type"]
            if type == "text":
                tag = block["data"]
            if type == "table":
                uid = block["uuid"]
                tag = f"table_{uid}"
            if type == "image":
                uid = block["uuid"]
                tag = f"image_{uid}"
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

    def blocks2html(self):
        for i, block in tqdm(enumerate(self.blocks)):
            style = block["style"]
            if style in self.STYLE_MAP:
                text = block["data"]
                bold = block.get("bold")
                size = block.get("size")
                if style == "image":
                    width = block.get("width", 100)
                    height = block.get("height", 100)
                    file_name = block.get("filename", uuid.uuid1().hex + ".png")
                    buffer_stream = convert_base64_to_buffer(b64_data=text)
                    if buffer_stream in self.images:
                        assert_url = self.images.get(buffer_stream,"")
                    else:
                        assert_url = upload_file(
                            file_name=file_name, file_stream=buffer_stream
                        )
                        self.images[buffer_stream] = assert_url
                    if not assert_url:
                        self.blocks[i]["html"] = ""
                        continue
                    block_html = self.text2html(
                        assert_url, style, width=width, height=height
                    )

                    block_markdown = self.text2markdown(text=assert_url, style=style)
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
                block_html = table.to_html(
                    index=False, justify="left", classes="mystyle", escape=False
                )

                block_markdown = table.to_markdown(index=False)
            else:
                text = block["data"]
                style = "Normal"
                bold = block.get("bold")
                size = block.get("size")
                block_html = self.text2html(text, style, font_size=size)
                if bold:
                    block_html = "<b>" + block_html + "</b>"
                    block_markdown = " **" + block_markdown + "**"
            self.blocks[i]["html"] = block_html
            self.blocks[i]["markdown"] = block_markdown


if __name__ == "__main__":

    file_path = "/Users/ucdteam/Downloads/test_files/育儿假东南区执行方案（流程版）20220413.docx"
    doc_loader = DocLoader(file_path=file_path)
    # print(doc_loader.tree)

    # for node in doc_loader.tree.all_nodes_itr():
    #     print(node)

    # q = "我想知道第一章的第二节的内容是什么？"
    # node = doc_loader.query_content_by_chapter_section(q)
    # print(node)
