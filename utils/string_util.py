# -*- coding: utf-8 -*-
"""
    @Time    : 2019/9/20 6:57 PM
    @Author  : alwin
"""
import re
import string

chinese_punc = "".join(
    [
        "“",
        "”",
        "‘",
        "’",
        "。",
        "，",
        "；",
        "：",
        "？",
        "！",
        "—",
        "～",
        "（",
        "）",
        "《",
        "》",
    ]
)

english_punc = "".join(
    ['"', '"', "'", "'", ".", ",", ";", ":", "?", "!", "-", "~", "(", ")", "<", ">"]
)


def string_full2half(string):
    """全角字符串转半角"""

    def full2half(char):
        """全角字符转半角"""
        code = ord(char)
        if code == 12288:  # 空格要特殊处理
            return chr(32)
        if 65281 <= code <= 65374:
            return chr(code - 65248)
        return char

    if string is None or not string.strip():
        return ""
    return "".join(map(full2half, list(string)))


def punc_chinese2english(string):
    """中文标点转英文"""
    tran_table = str.maketrans(chinese_punc, english_punc)
    return string.translate(tran_table)


def remove_punctuation(text):
    """移除文字中的索引标点符号"""
    puncs = chinese_punc + english_punc + string.punctuation + "…"
    return re.sub(rf"[{puncs}]", "", text)


def string_french2english(string):
    """法语字母转英语"""
    french_letters = "ÀàÂâÇçÉéÈèÊêËëÎîÏïÔôÛûÙùÜüŸÿ"
    enligsh_letters = "AaAaCcEeEeEeEeIiIiOoUuUuUuYy"
    tran_table = str.maketrans(french_letters, enligsh_letters)
    return string.translate(tran_table)


def normalize(s):
    for func in [string_full2half, string_french2english]:
        s = func(s)
    return s.strip()


def normalize2(s):
    for func in [string_full2half, punc_chinese2english, string_french2english]:
        s = func(s)
    return s.strip().upper()


def clear_text(s):
    m = re.sub(r"[\xa0\s]+", " ", s)
    m = m.strip(r'"\'•!@$^&(◆●■★·[]【】_-…—\\=~,;:<>?/ ＋←•→')
    return m


line_delimiter_reg = re.compile(
    "|".join(
        [
            "(([^\dA-Z&\- 大研第])(?P<post1>[1-9BDEFGH一二三四两][.、\) ]))",
            "(([^\dA-Z&\-大研第])(?P<post13>[1-9BDEFGH一二三四两][.、\)]))",
            "(([^\dA-Z&-])(?P<post11>[AC](([.、\)])|(\s+[^\/A-Z+\d]))))",
            "(([^\dA-Z&-])(?P<post12>[1-9]-[- ]+))",
            "([;!\n]+ *)",
            "(([^A-Z\.\d一二三四][.])(?P<post2>\n|[^NJ.]))",
            "((?P<pre1>([^*\-A-Z\d\s%一-龥])|([^\d\s][^\-A-Z*\d]))[*●◆■★•·-](?P<post3>[\s]*[\d一-龥]))",
            "((?P<pre11>[^*\-A-Z\d])[-](?P<post31>[\s]*[一-龥]))",
            "((?P<pre12>[1-9])-[-\s]+(?P<post32>[\s]*[\d一-龥]))",
            "((?P<pre2>[^*\-\d\s%A-Z一-龥])[-](?P<post4>[\s]*[\d一-龥]))",
            "((?P<pre21>[1-9])[-][-\s]+(?P<post41>[\s]*[\d一-龥]))",
        ]
    )
)

need_cat_start_reg1 = re.compile(r"[\(（][^)）]+$")
need_cat_end_reg1 = re.compile(r"^[^\(（]*[)）]")
need_cat_next_reg = re.compile(r"^\d+[.、)）]$")
num_reg = re.compile(r"\d$")
need_cat_next_reg2 = re.compile(r"((CET)|(NO.)|[和或与前])$")


def concat_line(content_cell, prev_line, content_cache):
    if (
        content_cell.startswith("、")
        or (
            need_cat_start_reg1.search(prev_line)
            and need_cat_end_reg1.search(content_cell)
        )
        or content_cell == "+"
        or prev_line == "+"
        or need_cat_next_reg2.search(prev_line)
    ):
        content_cache += content_cell
        prev_line += content_cell
    elif need_cat_next_reg.match(prev_line):
        content_cache += " "
        content_cache += content_cell
        prev_line += content_cell
    elif (
        prev_line.endswith("、")
        and content_cell
        and ord(prev_line[0]) + 1 != ord(content_cell[0])
    ):
        content_cache += content_cell
        prev_line += content_cell
    elif num_reg.search(prev_line) and num_reg.match(content_cell):
        content_cache += "-"
        content_cache += content_cell
        prev_line += content_cell
    else:
        return True, prev_line, content_cache
    return False, prev_line, content_cache


def broken_lines(s):
    s = normalize2(s)
    last_start_indx = 0
    prev_line = ""
    content_cache = ""
    # 序号开头, 或某些标点符号结尾,'- ',' -','* '
    for mat in re.finditer(line_delimiter_reg, s):
        span_start, span_end = mat.span()
        str_dict_to_keep = mat.groupdict()
        prefix = None
        postfix = None
        for k, v in str_dict_to_keep.items():
            if v:
                if "post" in k:
                    postfix = v
                elif "pre" in k:
                    prefix = v
        if prefix:
            span_end = span_start + len(prefix)
        elif postfix:
            span_end = span_end - len(postfix)
        x = s[last_start_indx:span_end]
        last_start_indx = span_end
        m = clear_text(x)
        if m:
            should_yield, prev_line, content_cache = concat_line(
                m, prev_line, content_cache
            )
            if should_yield:
                yield content_cache
                content_cache = m
                prev_line = m
    if last_start_indx < len(s):
        x = s[last_start_indx : len(s)]
        m = clear_text(x)
        if m:
            should_yield, prev_line, content_cache = concat_line(
                m, prev_line, content_cache
            )
            if should_yield:
                yield content_cache
                content_cache = m
                prev_line = m
    if content_cache:
        yield content_cache
        content_cache = ""
