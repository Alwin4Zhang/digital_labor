import os
import io
import sys
import re
import time
import uuid
import json
import shutil
import math
# import logging
from typing import Dict, List
from fuzzywuzzy import fuzz
import numpy as np

from langchain_core.output_parsers.json import parse_json_markdown

sys.path.append("./")

from configs.apollo_config import logger



from db.dao.knowledge_base_dao import (
    add_qa_to_db,
    add_document_to_db,
    update_qa_by_id,
    list_qas_from_db,
    delete_qa_from_db,
    get_qa_detail,
    get_document_state,
    get_document_detail,
)
from db.models.enum import KnowledgeSource, ReleaseStatus, UploadStatus, DocumentType,FileSource
from loader.unstructured_loaders.doc_loader import DocLoader
from loader.unstructured_loaders.pdf_loader import PDFLoader
from loader.unstructured_loaders.qa_loader import QALoader
from loader.unstructured_loaders.ppt_loader import PPTLoader
from loader.unstructured_loaders.table_loader import TableLoader
from textsplitter.document_header_splitter import document_header_splittor
from textsplitter.commonchs_text_splitter import commonchs_doc_splitter

from configs.apollo_config import SQLALCHEMY_DATABASE_URI
from configs.model_config import (
    QA_PROMPT,
    QA_FEW_SHOT_PROMPT,
    SPRAG_AUTO_CONTEXT_PROMPT,
    SECTION_SUMMARIZE_PROMPT,
    MAX_TOKENS
)

from configs.model_config import QA_FEW_SHOT_PROMPT_NAME_NAME,SPRAG_AUTO_CONTEXT_PROMPT_NAME,SECTION_SUMMARIZE_PROMPT_NAME,MAX_TOKENS,QA_PROMPT_NAME
from db.base import Base, create_engine, engine
from utils.llm_util import post_api_for_llm,post_api_for_llm_batch,get_num_tokens_from_messages
from utils.common import (
    convert_text_to_multilines,
    convert_file_type,
    convert_bytes_to_file,
    thread_parallel,
    timeit
)
from utils.traceback import langfuse

from db.models.enum import FileSource,Source
from db.service.milvus_chunk_db_service import default_chunk_db
from db.service.elasticsearch_kb_service import default_es_db
from db.embedding_utils import embed_texts_api

tmp_files_path = os.path.join(os.path.dirname(__file__), "tmp_files")
if not os.path.exists(tmp_files_path):
    os.mkdir(tmp_files_path)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)

Base.metadata.create_all(bind=engine)

markdown_re = re.compile(r"(\|[:]? [-]+ \|)|(\|[:]?[-]+\|)")  # 匹配markdown的份


def get_file_type(file_name):
    file_type = None
    if file_name.lower().endswith(".docx") or file_name.lower().endswith(".doc"):
        file_type = DocumentType.WORD
    elif file_name.lower().endswith(".pdf"):
        file_type = DocumentType.PDF
    elif file_name.lower().endswith(".ppt") or file_name.lower().endswith(".pptx"):
        file_type = DocumentType.PPT
    elif (
        file_name.lower().endswith(".xlsx")
        or file_name.lower().endswith(".xls")
        or file_name.lower().endswith(".csv")
        or file_name.lower().endswith(".tsv")
    ):
        file_type = DocumentType.EXCEL
    return file_type


def parse_doc_file_with_stream(
    file_name: str, file_stream: io.BytesIO = None, source=None,sprag_enhance: bool = False,**kwargs
):
    """解析文件流，目前覆盖:
    word:doc/docx;
    excel:xls/xlsx/csv;
    ppt:ppt/pptx
    """

    trace_id = kwargs.get("trace_id")
    user_id = kwargs.get("created_by")
    session_id = kwargs.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    module_name = kwargs.get("module_name","parse_document")

    def doc_splitter(doc_loader, use_header: bool = False):
        blocks = doc_loader.blocks
        # title = doc_loader.title
        # docs = document_header_splittor.split_text(blocks=blocks, use_header=use_header)
        docs = commonchs_doc_splitter.split_text(blocks=blocks)
        chunks = []
        for i, doc in enumerate(docs):
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
        # prompt = SPRAG_AUTO_CONTEXT_PROMPT.format(
        #     document_title=title, document=context
        # )
        prompt_template = langfuse.get_prompt(SPRAG_AUTO_CONTEXT_PROMPT_NAME)
        prompt = prompt_template.compile(
            document_title=title, document=context
        )
        token_nums = get_num_tokens_from_messages(prompt)
        if token_nums > MAX_TOKENS:
            for i in range(1,len(chunks),2):
                current_context = "\n".join([chunk.get("raw_text", "").strip() for chunk in chunks[:-i]])
                # prompt = SPRAG_AUTO_CONTEXT_PROMPT.format(
                #     document_title=title, document=current_context
                # )
                prompt = prompt_template.compile(
                    document_title=title, document=current_context
                )
                tk_nums = get_num_tokens_from_messages(prompt)
                if tk_nums <= MAX_TOKENS:
                    # prompt = current_context
                    break
        return post_api_for_llm(content=prompt,trace_id=trace_id,user_id=user_id,module_name=f"{module_name}-document-summary")

    def section_summary_enhance(chunk, title, i: any = None):
        """用文档段落生成一句话总结"""
        context = chunk.get("raw_text", "").strip()
        if not context:
            if i is not None:
                return (i, "")
            return ""
        # prompt = SECTION_SUMMARIZE_PROMPT.format(
        #     document_title=title, chunk_text=context
        # )
        prompt_template = langfuse.get_prompt(SECTION_SUMMARIZE_PROMPT_NAME)
        prompt = prompt_template.compile(
            document_title=title, chunk_text=context
        )
        res = post_api_for_llm(content=prompt,trace_id=trace_id,user_id=user_id,module_name=f"{module_name}-section-summary")
        if i is not None:
            res = (i, res)
        return res

    def get_chunk_header(doc_summary, section_summary):
        """获取chunk的header"""
        # return f"文档总结:{doc_summary}\n\n片段总结:{section_summary}"
        return f"片段总结:{section_summary}\n\n文档总结:{doc_summary}"

    def section_summary_enhance_parallel(chunks, title):
        """用文档段落生成一句话总结"""
        args_list = [(chunk, title, i) for i, chunk in enumerate(chunks)]
        return thread_parallel(section_summary_enhance, args_list)

    def sprag_enhance_func(chunks, title, parallel=True):
        """基于sprag思想增强chunk"""
        doc_summary = document_summary_enhance(chunks, title)
        if parallel:
            prompt_template = langfuse.get_prompt(SECTION_SUMMARIZE_PROMPT_NAME)
            prompts = [prompt_template.compile(
            document_title=title, chunk_text=chunk.get("raw_text", "").strip()) for chunk in chunks]
            results = post_api_for_llm_batch(prompts=prompts,
                                             trace_id=trace_id,
                                             user_id=user_id,
                                             module_name=f"{module_name}-section-summary"
                                             )
            # TODO: 尝试使用abatch async 可能会更快
            for i,result in enumerate(results):
                chunk_header = get_chunk_header(doc_summary, result)
                chunks[i]["raw_text_enhanced"] = chunk_header
            # results = section_summary_enhance_parallel(chunks=chunks, title=title)
            # for i, result in enumerate(results):
            #     idx, summary = result
            #     cur_chunk = chunks[idx]
            #     chunk_header = get_chunk_header(doc_summary, summary)
            #     # chunks[idx]["raw_text_enhanced"] = chunk_header + "\n\n" + cur_chunk["raw_text"]
            #     chunks[idx]["raw_text_enhanced"] = chunk_header
        else:
            i = 0
            while i < len(chunks):
                cur_chunk = chunks[i]
                section_summary = section_summary_enhance(cur_chunk, title)
                chunk_header = get_chunk_header(doc_summary, section_summary)
                # chunks[i]["raw_text_enhanced"] = chunk_header + "\n\n" + cur_chunk["raw_text"]
                chunks[i]["raw_text_enhanced"] = chunk_header
                i += 1

        return chunks

    res = None
    doc_loader = None
    file_type = get_file_type(file_name=file_name)
    
    if source == FileSource.KnowledgeQA:
        file_type = DocumentType.QA
    
    if file_type == DocumentType.WORD:
        # doc to docx
        if file_name.lower().endswith(".doc"):
            if file_stream is not None:
                save_path = os.path.join(tmp_files_path, file_name)
                convert_bytes_to_file(bytes_data=file_stream, file_path=save_path)
                file_name = save_path
            new_file_path = convert_file_type(
                doc_path=file_name,
                target_format="docx",
                output_directory=tmp_files_path,
            )
            if new_file_path:
                doc_loader = DocLoader(file_path=new_file_path, file_stream=None)
                if doc_loader.blocks:
                    os.remove(new_file_path)
                    os.remove(file_name)
        else:
            doc_loader = DocLoader(file_path=file_name, file_stream=file_stream)

        chunks = doc_splitter(doc_loader)
        title = doc_loader.maybe_title
        if sprag_enhance:
            # 文档全文生成一句话总结
            chunks = sprag_enhance_func(chunks, title)
        res = chunks
    elif file_type == DocumentType.PDF:
        doc_loader = PDFLoader(file_path=file_name, file_stream=file_stream)

        chunks = doc_splitter(doc_loader)
        title = doc_loader.maybe_title
        if sprag_enhance:
            # 文档全文生成一句话总结
            chunks = sprag_enhance_func(chunks, title)
        res = chunks
    elif file_type == DocumentType.EXCEL:
        doc_loader = TableLoader(file_path=file_name, file_stream=file_stream)
        chunks = doc_splitter(doc_loader)
        title = doc_loader.title
        if sprag_enhance:
            # 文档全文生成一句话总结
            chunks = sprag_enhance_func(chunks, title)
        res = chunks
    elif file_type == DocumentType.QA:
        qa_loader = QALoader(file_path=file_name, file_stream=file_stream)
        res = qa_loader.table2qas()

    elif file_type == DocumentType.PPT:
        # ppt to pptx
        if file_name.lower().endswith(".ppt"):
            if file_stream is not None:
                save_path = os.path.join(tmp_files_path, file_name)
                convert_bytes_to_file(bytes_data=file_stream, file_path=save_path)
                file_name = save_path
            new_file_path = convert_file_type(
                doc_path=file_name,
                target_format="pptx",
                output_directory=tmp_files_path,
            )
            if new_file_path:
                doc_loader = PPTLoader(file_path=new_file_path, file_stream=None)
                if doc_loader.blocks:
                    os.remove(new_file_path)
                    os.remove(file_name)
        else:
            doc_loader = PPTLoader(file_path=file_name, file_stream=file_stream)
            
        blocks = doc_loader.blocks
        chunks = []
        for i, block in enumerate(blocks):
            chunk = {
                "index": i,
                "raw_text": block.get("raw_text", ""),
                "html": block.get("html", ""),
                "metadata": {"Heading 1": block.get("title", "")},
            }
            chunks.append(chunk)
        title = doc_loader.maybe_title
        if sprag_enhance:
            # 文档全文生成一句话总结
            chunks = sprag_enhance_func(chunks, title)
        res = chunks

    return res, file_type


def upload_file_task(file_name, question_type, created_by, created_name,source=None):
    """初始化上传文件，生成document uuid"""
    file_type = get_file_type(file_name=file_name)
    assert file_type in [
        DocumentType.WORD,
        DocumentType.PDF,
        DocumentType.PPT,
        DocumentType.EXCEL,
    ]

    document_uuid = uuid.uuid1().hex
    # if source == Source.CREATE:
    #     source = FileSource.KnowledgeQA
    # if source == Source.FILE:
    #     source = FileSource.Document
        
    document_uuid = add_document_to_db(
        document_uuid=document_uuid,
        name=file_name,
        document_type=file_type,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
        source=source
    )
    if document_uuid:
        return document_uuid


def parse_document_to_db(
    document_uuid: str,
    file_name: str,
    file_stream: io.BytesIO = None,
    source: str = None,
    question_type: str = None,
    created_by: str = None,
    created_name: str = None,
    sprag_enhance: bool = False,
    trace_id: str=None
):
    """解析文档片段更新数据表"""
    try:
        res, file_type = parse_doc_file_with_stream(
            file_name=file_name, file_stream=file_stream, source=source,sprag_enhance=sprag_enhance,trace_id=trace_id
        )
        if res is not None:
            # 强制改为QA类型
            if file_type == DocumentType.EXCEL and source == FileSource.KnowledgeQA:
                file_type = DocumentType.QA
                source = Source.CREATE
            # 更新状态为已解析
            if file_type in [DocumentType.WORD, DocumentType.PPT, DocumentType.PDF,DocumentType.EXCEL]:
                document_uuid = add_document_to_db(
                    document_uuid=document_uuid,
                    chunks=res,
                    release_status=ReleaseStatus.PARSE_SUCCEED,
                )
                logger.info(
                    f"add parsed document :{file_name} into document table success!"
                )

                # 添加chunks到milvus
                # TODO:添加chunk to milvus chunk db vector index
                chunk_trans = []
                for i, chunk in enumerate(res):
                    chunk_trans.append(
                        {
                            "document_uuid": document_uuid,
                            "filename": file_name,
                            "chunk_id": chunk["index"],
                            "raw_text": chunk["raw_text"],
                            "raw_text_enhanced": chunk["raw_text_enhanced"]
                        }
                    )
                pks = default_chunk_db.do_add_doc(chunk_trans)
                logger.info(
                    f"insert document {file_name} chunks into default chunk db success,generate {len(pks)} chunks..."
                )
            elif file_type in [DocumentType.QA]:  # Excel直接写入qa
                if res:  # 表格中有内容
                    qa_ids = qa_generate_to_db(
                        document_uuid=document_uuid,
                        qas=res,
                        source=source,
                        question_type=question_type,
                        created_by=created_by,
                        created_name=created_name,
                    )
                    logger.info(
                        f"insert {len(qa_ids)} qas into knowledge table success!"
                    )

                    # 输入插入成功后，更新document状态为已解析
                    document_uuid = add_document_to_db(
                        document_uuid=document_uuid,
                        release_status=ReleaseStatus.PARSE_SUCCEED,
                    )
                else:  # 表格中无内容
                    document_uuid = add_document_to_db(
                        document_uuid=document_uuid,
                        release_status=ReleaseStatus.PARSE_FAILED,
                    )
        else:  # 文档解析无内容，直接置为FAIL
            document_uuid = add_document_to_db(
                document_uuid=document_uuid,
                chunks=[],
                release_status=ReleaseStatus.PARSE_FAILED,
            )
    except Exception as e:
        logger.error(e)
        document_uuid = add_document_to_db(
            document_uuid=document_uuid, release_status=ReleaseStatus.PARSE_FAILED
        )
    return document_uuid


@timeit
def qa_generate_to_db(
    document_uuid,
    qas: List = None,
    source: str = None,
    question_type: str = None,
    interval: int = 5,
    created_by: str = None,
    created_name: str = None,
    **kwargs
):
    trace_id = kwargs.get("trace_id")
    user_id = kwargs.get("created_by")
    session_id = kwargs.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    module_name = kwargs.get("module_name","qa_generate")

    def qa_pair_generate(context, default_num: int = 5):
        # from configs.model_config import QA_PROMPT

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
            # prompt_template = QA_PROMPT
            prompt_template = langfuse.get_prompt(QA_PROMPT)
            has_table = check_table(context)
            if has_table:
                # prompt_template = QA_FEW_SHOT_PROMPT
                prompt_template = langfuse.get_prompt(QA_FEW_SHOT_PROMPT)
            # prompt = prompt_template.format(context=context, num=num)
            prompt = prompt_template.compile(context=context, num=num)
            # response = post_api_for_llm(content=prompt)
            response = post_api_for_llm(content=prompt,
                                        trace_id=trace_id,
                                        user_id=user_id,
                                        module_name=f"{module_name}"
                                        )
            res = parse_json_markdown(response)
            return res
        except Exception as e:
            logger.error(e)
        return res

    ct = 0
    early_stop = False
    while 1:
        if qas:
            break
        # 查询数据表状态
        doc = get_document_detail(document_uuid=document_uuid)
        release_status = doc.get("release_status")
        # 如果是解析失败，则break
        if release_status in [
            ReleaseStatus.PARSE_FAILED,
            # ReleaseStatus.QA_GENERATING,
            ReleaseStatus.QA_AWAIT,
            ReleaseStatus.QA_RELEASED,
        ]:
            return
        
        if release_status is None or release_status not in [
            ReleaseStatus.PARSE_SUCCEED,
            ReleaseStatus.QA_GENERATED_FAILED,
        ]:
            time.sleep(interval)
            ct += 1
            if ct > 100:
                early_stop = True
                break
            continue
        chunks = doc.get("chunks")
        if not chunks:
            break
        # 解析chunk to qas
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
                answer = convert_text_to_multilines(pair[1]).strip()
                qas.append(
                    {
                        "chunk_index": chunk_index,
                        "question": pair[0],
                        "answer": answer,
                        "answer_markdown": answer,
                    }
                )
        break
        # args_list = [(chunk["raw_text"],i) for i,chunk in enumerate(chunks)]
        # results = thread_parallel(qa_pair_generate, args_list)
        # for i,result in enumerate(results):
        #     if not isinstance(result, tuple):
        #         continue
        #     idx, qa_pairs = result
        #     logger.info(f"generate qa pairs for chunk {qa_pairs} success!")
        #     cur_chunk = chunks[idx]
        #     for qa in qa_pairs:
        #         if not isinstance(qa, dict):
        #             continue
        #         pair = list(qa.values())
        #         if len(pair) < 2:
        #             continue
        #         qas.append(
        #             {
        #                 "chunk_index": cur_chunk["index"],
        #                 "question": pair[0],
        #                 "answer": convert_text_to_multilines(pair[1]),
        #             }
        #         )
    """生成qa对"""
    qa_ids = []
    # TODO: qas去重，有的时候会有重复的qa
    qa_dups = {}
    
    # if qas == []: # 文档没有生成QA
    #     add_document_to_db(
    #         document_uuid=document_uuid, 
    #         release_status=ReleaseStatus.QA_AWAIT
    #     )
    #     return qa_ids
        
    qas = qas if qas else []
    for qa in qas:
        question = qa.get("question")
        answer = qa.get("answer")
        answer_markdown = (
            qa.get("answer_markdown") if qa.get("answer_markdown") else answer
        )
        question_type = (
            qa.get("question_type") if qa.get("question_type") else question_type
        )
        chunk_index = qa.get("chunk_index")
        if not question and not answer:
            continue
        if question in qa_dups:
            continue
        qa_dups[question] = 1

        if source == FileSource.KnowledgeQA:
            source = Source.CREATE
        elif source == FileSource.Document:
            source = Source.FILE

        qa_id = add_qa_to_db(
            document_uuid=document_uuid,
            source=source,
            type=question_type,
            question=question,
            answer=answer,
            chunk_index=chunk_index,
            created_by=created_by,
            created_name=created_name,
            answer_markdown=answer_markdown,
        )
        qa_ids.append(qa_id)

    # 更新document状态为待发布
    if qa_ids:
        add_document_to_db(
            document_uuid=document_uuid, 
            release_status=ReleaseStatus.QA_AWAIT
        )
    if early_stop or not qa_ids:
        add_document_to_db(
            document_uuid=document_uuid, 
            release_status=ReleaseStatus.QA_GENERATED_FAILED
        )
    return qa_ids


@timeit
def qa_release_valiate(docs: List[Dict] = None, threshold: int = 95):
    """QA发布前的校验: docs的基础字段：id,question,answer,document_uuid,released_status
    现在的问题：
    待发布问题重复校验:
        1.单个文档内的重复
        2.文档间的
    待发布与已发布重复校验:
        3.单个文档与已发布的重复
    """
    docs = sorted(docs, key=lambda x: x.get("document_uuid"))

    @timeit
    def es_question_validate(question, threshold=threshold):
        """es库中问题重复校验"""
        dsl = {
            "_source": {"excludes": ["question_vector"]},
            "from": 0,
            "size": 20,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "question": {
                                    "query": question,
                                    "analyzer": "ikSearchAnalyzer",
                                }
                            }
                        }
                    ]
                }
            },
        }
        hits = default_es_db.do_search(question, dsl=dsl)
        candidates = [
            (
                hit["_id"],
                hit["_source"]["question"],
                hit["_source"]["answer"],
                hit["_source"].get("document_uuid"),
            )
            for hit in hits
        ]

        res = []

        for _id, q, a, duuid in candidates:
            simi_score = fuzz.ratio(question, q)
            if simi_score >= threshold:
                res.append(
                    {
                        "id": int(_id),
                        "question": q,
                        "answer": a,
                        "document_uuid": duuid,
                        "release_status": ReleaseStatus.QA_RELEASED,
                        # "score": simi_score,
                    }
                )
        return res

    @timeit
    def inner_validate(docs, threshold=threshold):
        """
        inner_res : list，每个值是一个问题和其相似的若干问题
        rest_docs: 聚合重复后和剩余的文档合并
        """
        inner_res, rest_docs = [], []

        uses_d = {}

        for i in range(len(docs)):
            if len(uses_d) == len(docs):
                break
            cur_doc = docs[i]
            cur_doc_id = cur_doc.get("id")
            cur_doc_question = str(cur_doc.get("question")).strip()
            if cur_doc_id in uses_d:
                continue
            if not cur_doc_question:
                continue
            tp_similar_question = []
            for j in range(i + 1, len(docs)):
                d = docs[j]
                _id = d.get("id")
                if _id in uses_d:
                    continue
                dq = str(d.get("question")).strip()
                simi_score = fuzz.ratio(cur_doc_question, dq)
                if simi_score < threshold:
                    continue
                tp_similar_question.append(d)
                uses_d[_id] = 1
            if tp_similar_question:
                uses_d[cur_doc_id] = 1
                cur_doc.update({"similar_question": tp_similar_question})
                inner_res.append(cur_doc)

        rest_docs = inner_res + [doc for doc in docs if doc.get("id") not in uses_d]
        return inner_res, rest_docs


    @timeit
    def inner_validate2(docs,threshold=threshold):
        """
        通过向量计算相似度+editdistance过滤
        先计算相似度，再用编辑距离过滤
        """
        texts = [doc.get("question") for doc in docs if doc.get("question")]
        embs = embed_texts_api(texts,return_numpy=True)
        sim = np.tril(embs @ embs.T,-1)
        above_pairs = np.where(sim > threshold/100)
        d_res,uses_d= {},{}
        for x,y in zip(above_pairs[0].tolist(),above_pairs[1].tolist()):
            if y in uses_d:
                continue
            simi_score = fuzz.ratio(docs[x]['question'],docs[y]['question'])
            if simi_score <= threshold:
                continue
            if x not in d_res:
                d_res[x] = [y]
            else:
                d_res[x].append(y)
            uses_d[y] = 1
        for k,v in d_res.items():
            docs[k].update({"similar_question": [docs[i] for i in v]})
        return docs
    
    @timeit
    def es_questions_validate(questions,threshold=threshold):
        def do_search(i, q, dsl):
            hits = default_es_db.do_search(question, dsl=dsl)
            """
             "id": 30634,
            "documentUuid": "cd9b7bc224a111f080617233a72c882c",
            "chunkIndex": "1",
            "question": "本报告是美新科技股份有限公司发布的第几份年度可持续发展报告？",
            "answer": "本报告是美新科技股份有限公司发布的第1份年度可持续发展报告.",
            "answerMarkdown": "本报告是美新科技股份有限公司发布的第1份年度可持续发展报告.",
            "questionType": "行政",
            "releaseStatus": "qa_await",
            "documentName": "美新科技：2024年度环境、社会与公司治理（ESG）报告.pdf"
            """
            # candidates = [(hit["_id"], hit["_source"]["question"]) for hit in hits]
            qids = [str(doc.get("id")) for doc in docs if doc.get("id")]
            candidates = [{
                "id": int(hit["_id"]),
                "question": hit["_source"]["question"],
                "answer": hit["_source"]["answer"],
                "document_uuid": hit["_source"].get("document_uuid"),
                "release_status": ReleaseStatus.QA_RELEASED
            } for hit in hits if str(hit["_id"]) not in qids]
            ncands = []
            for c in candidates:
                qc = c['question']
                simi_score = fuzz.ratio(q, qc)
                if simi_score >= threshold:
                    ncands.append(c)
            if not ncands:
                return i,[]
            embs = embed_texts_api([q.get("question","") for q in ncands],return_numpy=True)
            emb_q = embed_texts_api(q,return_numpy=True)
            sim = emb_q @ embs.T
            idxs_tuples = np.where(sim > threshold / 100)
            return i,[candidates[idx] for idx in idxs_tuples[-1]]
        
        actions = []
        for i,question in enumerate(questions):
            dsl = {
                "_source": {"excludes": ["question_vector"]},
                "from": 0,
                "size": 20,
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "question": {
                                        "query": question,
                                        "analyzer": "ikSearchAnalyzer",
                                    }
                                }
                            }
                        ]
                    }
                },
            }
            actions.append((i,question,dsl))
        return thread_parallel(do_search,args_list=actions)
        
    res = []
    # inner_res, rest_docs = inner_validate(docs)
    # 内部校验重复
    docs = inner_validate2(docs)
    res.extend([d for d in docs if "similar_question" in d])

    inner_dict = {doc['id']:doc for doc in docs if "similar_question" in doc}

    results = es_questions_validate(questions=[str(doc.get("question")).strip() for doc in docs
     if str(doc.get("question")).strip()])
    for result in results:
        idx,candidates = result
        doc = docs[idx]
        _id = doc["id"]
        if _id in inner_dict:
            if candidates:
                esimilar_question = [q for q in candidates if q[0] != _id]
                esimilar_question = (
                    inner_dict[_id].get("similar_question", []) + esimilar_question[:]
                )
                idx = res.index(inner_dict[_id])
                inner_dict[_id]["similar_question"] = esimilar_question[:]
                res[idx] = inner_dict[_id]
        else:
            doc.update({"similar_question": candidates})
            res.append(doc)
    
    # flatten
    similar_groups = []
    for r in res:
        _id = r.get("id")
        similar_questions = r.get("similar_question", [])
        r.pop("similar_question")
        similar_questions = [q for q in similar_questions if q.get("id") != _id]
        if similar_questions:
            similar_groups.append([r] + similar_questions)
        else:
            similar_groups.append([r])
    return similar_groups



        

    # 旧代码
    # inner_dict = {r["id"]: r for r in inner_res}
    # res.extend(inner_res[:])

    # 与已有的es库保存的数据校验重复
    # 注意：可能是已发布过的问题二次修改，导致校验命中，需要将
    # for doc in rest_docs:
    #     _id = doc.get("id")
    #     question = str(doc.get("question")).strip()
    #     if not question:
    #         continue
    #     esimilar_question = es_question_validate(question=question)

    #     # 与前两种相似的合并
    #     if _id in inner_dict:
    #         if esimilar_question:
    #             # 过滤掉已发布id重复的问题，允许二次修改后上传
    #             esimilar_question = [q for q in esimilar_question if q["id"] != _id]
    #             esimilar_question = (
    #                 inner_dict[_id].get("similar_question", []) + esimilar_question[:]
    #             )
    #             idx = res.index(inner_dict[_id])
    #             inner_dict[_id]["similar_question"] = esimilar_question[:]
    #             res[idx] = inner_dict[_id]
    #     else:
    #         doc.update({"similar_question": esimilar_question})
    #         res.append(doc)

    # # 所有数据全部flatten

    # for r in res:
    #     _id = r.get("id")
    #     similar_questions = r.get("similar_question", [])
    #     r.pop("similar_question")
    #     similar_questions = [q for q in similar_questions if q.get("id") != _id]
    #     if similar_questions:
    #         similar_groups.append([r] + similar_questions)
    #     else:
    #         similar_groups.append([r])

    # return similar_groups
