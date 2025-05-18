import os
import re

ZH_REG = re.compile(r"[一-龢]+")
heading1_reg = re.compile(r"(^[0-9]+[、.])|(^[一二三四五六七八九十]+[、.])")
heading2_reg = re.compile(
    r"(^[(（][一二三四五六七八九十]+[)）][、.]?)|(^[0-9]+[、.][0-9]+)"
)
heading3_reg = re.compile(r"^[0-9]+[、.][0-9]+[、.][0-9]+")
heading4_reg = re.compile(r"^[0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+")
heading5_reg = re.compile(r"^[0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+")
heading6_reg = re.compile(
    r"^[0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+[、.][0-9]+"
)

whitespace_reg = re.compile(r"[\s\xa0\u3000\u2002\u2003]+")

chapter_reg = re.compile(r"[第]([0-9一二三四五六七八九十])+章")
section_reg = re.compile(r"[第]([0-9一二三四五六七八九十])+节")
subsection_reg = re.compile(r"[第]([0-9一二三四五六七八九十])+小节")

heading_levels = {
    "Title": 0,
    "Heading 1": 1,
    "Heading 2": 2,
    "Heading 3": 3,
    "Heading 4": 4,
    "Heading 5": 5,
    "Heading 6": 6,
    "Normal": 10,
}

NORMAL = "Normal"
TITLE = "Title"
HEADING1 = "Heading 1"
HEADING2 = "Heading 2"
HEADING3 = "Heading 3"
HEADING4 = "Heading 4"
HEADING5 = "Heading 5"
HEADING6 = "Heading 6"


# 认为是非正式文件名称,不作为文件名称，从文档的前几页找标题
TEST_FILENAMES = re.compile(
    r"^" + "|".join(["test", "测试文[稿档]", "文字文[稿档]", "工作簿", "演示文[稿档]", "未命名"])
)