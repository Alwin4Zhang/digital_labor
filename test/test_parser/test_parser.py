# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2025/04/17 14:51:35
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''
import sys
sys.path.append("./")
sys.path.append("../")

import re
import time
from loader.unstructured_loaders.pdf_loader import PDFLoader
from loader.unstructured_loaders.table_loader import TableLoader
from loader.unstructured_loaders.doc_loader import DocLoader
from loader.unstructured_loaders.ppt_loader import PPTLoader
from utils.common import get_file_type
from db.models.enum import DocumentType

from typing import Dict, List

from textsplitter.commonchs_text_splitter import commonchs_doc_splitter
from configs.model_config import SPRAG_AUTO_CONTEXT_PROMPT,SECTION_SUMMARIZE_PROMPT,MAX_TOKENS,QA_PROMPT,QA_FEW_SHOT_PROMPT
from utils.llm_util import get_num_tokens_from_messages,post_api_for_llm,post_api_for_llm_batch
from langchain_core.output_parsers.json import parse_json_markdown
from db.dao.knowledge_base_dao import get_document_detail
from db.models.enum import KnowledgeSource, ReleaseStatus, UploadStatus, DocumentType,FileSource



def test_parse(filename):
    file_type = get_file_type(filename)
    if file_type == DocumentType.WORD:
        loader = DocLoader(filename)
    if file_type == DocumentType.PDF:
        loader = PDFLoader(filename)
    if file_type == DocumentType.PPT:
        loader = PPTLoader(filename)
    if file_type == DocumentType.EXCEL:
        loader = TableLoader(filename)

    blocks = loader.blocks

    # print(blocks)
    return blocks

def qa_generate_to_db(
    chunks
):
    markdown_re = re.compile(r"(\|[:]? [-]+ \|)|(\|[:]?[-]+\|)")  # 匹配markdown的份

    def qa_pair_generate(context, default_num: int = 5):
        from configs.model_config import QA_PROMPT

        """qa生成"""
        res = []
        try:

            def check_table(content):
                """校验content中是否有markdown表格"""
                return bool(markdown_re.search(content))

            def question_num(context, default_length=50):
                """
                1.如果是多行文本，则按照行数来确定
                2.如果大于100个字，则按照字数整除数生成
                """
                num = len([l for l in context.splitlines() if l.strip()]) // 2
                if num > 0:
                    return num
                div_r = len(context) // default_length
                if div_r >= 1:
                    return div_r if div_r < default_num else default_num
                return 0

            num = question_num(context=context)
            if num == 0:
                return []
            # 判断是否含有表格内容，如果有表格则转为markdown后使用few_shot_prompt
            prompt_template = QA_PROMPT
            has_table = check_table(context)
            if has_table:
                prompt_template = QA_FEW_SHOT_PROMPT
            prompt = prompt_template.format(context=context, num=num)
            response = post_api_for_llm(content=prompt)
            res = parse_json_markdown(response)
            return res
        except Exception as e:
            print(e)
        return res
    qas = []
    for i, chunk in enumerate(chunks):
        chunk_index = chunk["index"]
        qa_pairs = qa_pair_generate(context=chunk["raw_text"])
        for qa in qa_pairs:
            if not isinstance(qa, dict):
                continue
            pair = list(qa.values())
            if len(pair) < 2:
                continue
            answer = pair[1]
            qas.append(
                {
                    "chunk_index": chunk_index,
                    "question": pair[0],
                    "answer": answer,
                    "answer_markdown": answer,
                }
            )
    return qas

def test_pipeline(filename):

    def doc_splitter(blocks):
        documents = commonchs_doc_splitter.split_text(blocks=blocks)
        chunks = []
        for i, doc in enumerate(documents):
            page_content = doc.page_content
            metadata = doc.metadata
            chunk = {
                "index": i,
                # "raw_text": metadata.get("chunk_raw_text"),
                "raw_text": page_content,
                "raw_text_enhanced": page_content,
                "html": metadata.get("html", ""),
                "metadata": metadata,
            }
            chunks.append(chunk)
        return chunks

    def document_summary_enhance(chunks, title):
        """用文档全文生成一句话总结"""
        context = "\n".join([chunk.get("raw_text", "").strip() for chunk in chunks])
        prompt = SPRAG_AUTO_CONTEXT_PROMPT.format(
            document_title=title, document=context
        )
        token_nums = get_num_tokens_from_messages(prompt)
        if token_nums > MAX_TOKENS:
            for i in range(1,len(chunks),2):
                current_context = "\n".join([chunk.get("raw_text", "").strip() for chunk in chunks[:-i]])
                prompt = SPRAG_AUTO_CONTEXT_PROMPT.format(
                    document_title=title, document=current_context
                )
                tk_nums = get_num_tokens_from_messages(prompt)
                if tk_nums <= MAX_TOKENS:
                    # prompt = current_context
                    break
        return post_api_for_llm(content=prompt)

    def get_chunk_header(doc_summary, section_summary):
        """获取chunk的header"""
        # return f"文档总结:{doc_summary}\n\n片段总结:{section_summary}"
        return f"片段总结:{section_summary}\n\n文档总结:{doc_summary}"

    def section_summary_enhance(chunk, title, i: any = None):
        """用文档段落生成一句话总结"""
        context = chunk.get("raw_text", "").strip()
        if not context:
            if i is not None:
                return (i, "")
            return ""
        prompt = SECTION_SUMMARIZE_PROMPT.format(
            document_title=title, chunk_text=context
        )
        res = post_api_for_llm(content=prompt)
        if i is not None:
            res = (i, res)
        return res


    def sprag_enhance_func(chunks,title):
        doc_summary = document_summary_enhance(chunks, title)
        prompts = [SECTION_SUMMARIZE_PROMPT.format(
        document_title=title, chunk_text=chunk.get("raw_text", "").strip()) for chunk in chunks]
        results = post_api_for_llm_batch(prompts=prompts)
        # TODO: 尝试使用abatch async 可能会更快
        for i,result in enumerate(results):
            chunk_header = get_chunk_header(doc_summary, result)
            chunks[i]["raw_text_enhanced"] = chunk_header
        return chunks
        
    blocks = test_parse(filename)
    chunks = doc_splitter(blocks[:])
    chunks = sprag_enhance_func(chunks,filename)

    # qas = qa_generate_to_db(chunks=chunks)

    return chunks



if __name__ == '__main__':
    abs_path = "./test/test_files/6.1.2.1.1 超市DM选品规范.pdf"
    abs_path = "./test/test_files/6、超市门店员工岗位操作手册（花艺助理）1.pdf"
    
    # abs_path= "/Users/ucdteam/Downloads/1222805483.pdf"
    abs_path = "/Users/ucdteam/Downloads/1223306972.pdf"
    
    abs_path = "/Users/ucdteam/Downloads/中航科创有限公司国内公务接待管理规定.pdf"
    
    # abs_path = "/Users/ucdteam/Downloads/yangshan96_my_data_set.tsv"
    
    # table_loader = TableLoader(
    #     file_path=abs_path
    # )
    
    # blocks = table_loader.blocks
    
    # abs_path = "/Users/ucdteam/Desktop/metrics.xlsx"
    # abs_path = "/Users/ucdteam/Downloads/中航科创-安哥拉工程项目税务测算模型_20200405.xlsx"
    
    
    
    # excel_loader = TableLoader(
    #     file_path=abs_path   
    # )
    # blocks = excel_loader.blocks
    # with open("test.txt","a+") as wf:
    #     for blk in blocks:
    #         # print(blk['markdown'])
            # wf.write(blk['markdown'] + "\n\n")

    abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/附件1：管理类档案归档范围与保管期限表.docx"
    # abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/附件.中航科创所属单位全面风险管理与内部控制体系建设指引.docx"

    # abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/中航科创有限公司党委党建工作考核评价办法.pdf"
    # abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/中航科创有限公司纪委向党委请示报告工作管理办法.pdf"
    # abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/中航科创-安哥拉税收管理手册 - 税务场景_20200331.pdf"
    # abs_path = "/Users/ucdteam/Downloads/中航科创-badcase/中航科创-安哥拉税收管理手册 - 税务决策_20200331.pdf"

    # blocks = test_parse(abs_path)


    
    
    # abs_path = "/Users/ucdteam/Downloads/中航科创-埃塞俄比亚EPC税务管理手册 - 税制介绍 - 20191219.pdf"
    # pdf_loader = PDFLoader(
    #     file_path=abs_path
    # )
    
    # blocks = pdf_loader.blocks
    # documents = commonchs_doc_splitter.split_text(blocks=blocks)

    abs_path = "/Users/ucdteam/Downloads/解析失败文件/私域运营专员岗位手册.pdf"

    documents = test_pipeline(abs_path)
    
    print(documents)