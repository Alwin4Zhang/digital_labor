import sys
import re
import time
import copy

sys.path.append("./")

import datetime
import asyncio
from typing import List
from functools import lru_cache
from abc import ABC, abstractmethod

import numpy as np
from tqdm import tqdm

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from fuzzywuzzy import fuzz

from configs.model_config import *
from configs.apollo_config import MODEL_NAME_QWEN2HALF_7B 
from db.models.enum import ReleaseStatus, GradeScore
from db.service.milvus_kb_service import default_vector_db
from db.service.milvus_chunk_db_service import default_chunk_db
from db.service.elasticsearch_kb_service import default_es_db
from db.dao.knowledge_base_dao import get_document_detail, get_document_chunks
from utils.llm_util import post_api_for_llm, apost_api_for_llm, post_api_for_llm_batch
from utils.traceback import langfuse
from db.embedding_utils import embed_texts_api, embed_documents_api, rerank_texts_api
from configs.apollo_config import logger


class LocalHybridRag(object):
    top_k = VECTOR_SEARCH_TOP_K
    score_threshold = VECTOR_SEARCH_SCORE_THRESHOLD

    def __init__(self) -> None:
        pass

    def streaming_simu_output(
        self,
        query,
        content,
        chat_history=None,
        related_docs=None,
        interval=0.02,
        limit=500,
    ):
        """
        模拟对话系统的输出，基于语言模型的多轮对话。
        更好的方式，是使用tokenizer来切分token
        """

        resp = ""
        if not chat_history:
            chat_history = []

        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": ""})
        wait = False
        if len(content) <= limit:
            wait = True
        for i, token in enumerate(content):
            if wait:
                time.sleep(interval)
            resp += token
            if i <= 5:
                resp = resp.lstrip()

            chat_history[-1] = {"role": "assistant", "content": resp}
            # chat_history[-2] = {"role": "user", "content": query}

            response = {
                "knowledge_id": (
                    related_docs[0]["knowledge_id"] if related_docs else None
                ),
                "query": query,
                "result": resp,
                "source_documents": related_docs,
            }

            yield response, chat_history

    def streaming_llm_output(
        self, query, chat_history=None, related_docs=None, original_query=None,**kwargs
    ):
        trace_id = kwargs.get("trace_id")
        user_id = kwargs.get("created_by")
        session_id = kwargs.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
        module_name = kwargs.get("module_name","dialog")

        """使用大模型做回复"""
        if chat_history is None:
            chat_history = []
        stream_resp = ""
        for inum, chunk in enumerate(apost_api_for_llm(content=query,
                                                       trace_id=trace_id,
                                                       user_id=user_id,
                                                       session_id=session_id,
                                                       module_name=module_name)):
            if inum == 0:
                chat_history.append(
                    {
                        "role": "user",
                        # "content": query if original_query is None else original_query,
                        "content": original_query,
                    }
                )
                chat_history.append({"role": "assistant", "content": ""})
            stream_resp += chunk if chunk else ""

            chat_history[-1] = {"role": "assistant", "content": stream_resp}

            response = {
                "knowledge_id": None,
                "query": query if original_query is None else original_query,
                "result": stream_resp,
                "source_documents": related_docs if related_docs else [],
            }
            yield response, chat_history

    def dialog_format(self, query, chat_history):
        """
        对话系统的对话格式化模块，将历史对话列表，转换为大模型需要的输入格式。
        Args:
            query (str): 用户输入的查询语句
            chat_history (list): 历史对话列表，每个元素为(query, answer)的元组

        Returns:
            str : 大模型提示词的输入格式
        """
        dialog = ""

        for i, turn in enumerate(chat_history):
            role = turn.get("role")
            content = turn.get("content")

            if role == "user":
                # dialog += f"A{i // 2 + 1}: {content}  "
                dialog += f"Q{i // 2 + 1}: {content}" + "\n"
            elif role == "assistant":
                # dialog += f"B{i // 2 + 1}: {content}" + "\n"
                dialog += f"A{i // 2 + 1}: {content}" + "\n"

        # dialog += f"A{len(chat_history) // 2 + 1}: {query}"
        dialog += f"Q{len(chat_history) // 2 + 1}: {query}"

        return dialog

    def rewrite_format(self, query, chat_history):
        """
        对话系统的对话格式化模块，将历史对话列表，转换为大模型需要的输入格式。
        Args:
            query (str): 用户输入的查询语句
            chat_history (list): 历史对话列表，每个元素为(query, answer)的元组

        Returns:
            str : 大模型提示词的输入格式
        """
        # 你是一个擅长对给定的历史对话记录整理成问题的专家。根据历史对话记录，重写用户的完整问题，只生成问题。
        history_context = ""
        for i, turn in enumerate(chat_history):
            role = turn.get("role")
            content = turn.get("content")

            # if role == "user":
            #     history_context += f"问题: {content}  "
            # elif role == "assistant":
            #     history_context += f"回答: {content}" + "\n"
            if role == "user":
                history_context += f"Q: {content}" + "\n"
            elif role == "assistant":
                # dialog += f"B{i // 2 + 1}: {content}" + "\n"
                history_context += f"A: {content}" + "\n"
            

        return langfuse.get_prompt(REWRITE_QUESTION_PROMPT_NAME).compile(history_context=history_context, current_question=query)
        # return REWRITE_QUESTION_PROMPT.format(
        #     history_context=history_context, current_question=query
        # )

    def chunks_to_raw_content(self, chunks):
        """
        将chunk列表转换为原始文档内容
        """
        raw_content = ""
        for chunk in chunks:
            raw_content += chunk.get("raw_text") + "\n"
        return raw_content
    
    def HyDE(self,query,**kwargs):
        trace_id = kwargs.get("trace_id")
        user_id = kwargs.get("created_by")
        session_id = kwargs.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
        module_name = kwargs.get("module_name","dialog")

        prompt = langfuse.get_prompt(HYDE_PROMPT_NAME).compile(question=query)
        return post_api_for_llm(
            content=prompt,
            model_name=MODEL_NAME_QWEN2HALF_32B,
            trace_id=trace_id,
            user_id=user_id,
            session_id=session_id,
            module_name=f"{module_name}-HyDE"
        )

    def dialog_onetune(self, query, chat_history,**kwargs):
        """
        对话系统的One-Tune模块，基于语言模型的多轮对话。
        :param query: 用户输入的查询语句
        :param chat_history: 历史对话列表，每个元素为(query, answer)的元组
        """
        # TODO: 可以优化的点，query向量化可以只调用一次，不用每次都调用
        trace_id = kwargs.get("trace_id")
        user_id = kwargs.get("created_by")
        session_id = kwargs.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
        module_name = kwargs.get("module_name","dialog")

        def retrieve_and_rag(query, chat_history=None, original_query=None):
            query_vector = embed_texts_api(query)
            related_docs = default_vector_db.do_search(
                # query=query,
                score_threshold=self.score_threshold,
                release_status=ReleaseStatus.QA_RELEASED,
                query_vector=query_vector,
            )

            if not related_docs:
                # TODO：同时使用问题-文本块和虚拟答案-文本块的召回
                hyde_answer = self.HyDE(query=query)
                # 进行相似块的召回，或者用基于相似块所在的文档回答当前问题
                related_chunks = default_chunk_db.do_search(
                    # query=query,
                    # score_threshold=self.score_threshold,
                    query_vector=query_vector,
                )

                related_chunks_hyde = default_chunk_db.do_search(
                    query=hyde_answer
                )

                related_chunks += related_chunks_hyde
                if not related_chunks:  # 兜底话术
                    # safty_prompt = GREETING_QUESTION_PROMPT.format(
                    #     default_response=DEFAULT_RESPONSE, question=original_query
                    # )
                    safty_prompt = langfuse.get_prompt(GREETING_QUESTION_PROMPT_NAME).compile(
                        default_response=DEFAULT_RESPONSE, question=original_query
                    )
                    return self.streaming_llm_output(
                        query=safty_prompt,
                        chat_history=chat_history,
                        related_docs=[],
                        original_query=original_query,
                    )

                # Rerank
                # related_chunk_raw_texts = [chunk.get("raw_text","") for chunk in related_chunks]
                # related_chunk_raw_texts = rerank_texts_api(query, related_chunk_raw_texts,verbose=True)

                # CRAG cover
                most_similar_chunk, idx = None, None

                related_chunks_prompts = []
                for i, related_chunk in enumerate(related_chunks):
                    related_chunk_raw_text = related_chunk.get("raw_text", "")
                    # prompt_crag = CRAG_PROMPT.format(
                    #     context=related_chunk_raw_text, question=query
                    # )
                    prompt_crag = langfuse.get_prompt(CRAG_PROMPT_NAME).compile(
                        context=related_chunk_raw_text, question=query
                    )
                    related_chunks_prompts.append(prompt_crag)

                related_chunks_grade_scores = post_api_for_llm_batch(
                    prompts=related_chunks_prompts,
                    model_name=MODEL_NAME_QWEN2HALF_32B ,
                    trace_id=trace_id,
                    user_id=user_id,
                    session_id=session_id,
                    module_name=f"{module_name}-crag",
                    max_concurrency=2
                )
                for i, related_chunk_grade_score in enumerate(
                    related_chunks_grade_scores
                ):
                    if related_chunk_grade_score == GradeScore.YES:
                        most_similar_chunk = related_chunks[i]
                        idx = i
                        break

                # change not related chunks
                related_chunks = related_chunks[idx:]

                document_detail, chunks = None, None

                if most_similar_chunk:
                    document_detail = get_document_detail(
                        document_uuid=most_similar_chunk.get("document_uuid")
                    )
                    if document_detail:
                        chunks = document_detail.get("chunks")

                if (
                    not most_similar_chunk or not document_detail or not chunks
                ):  # 兜底话术
                    # safty_prompt = GREETING_QUESTION_PROMPT.format(
                    #     default_response=DEFAULT_RESPONSE, question=original_query
                    # )
                    safty_prompt = langfuse.get_prompt(GREETING_QUESTION_PROMPT_NAME).compile(
                        default_response=DEFAULT_RESPONSE, question=original_query
                    )
                    return self.streaming_llm_output(
                        query=safty_prompt,
                        chat_history=chat_history,
                        related_docs=[],
                        original_query=original_query,
                    )
                doc_raw_content = self.chunks_to_raw_content(chunks)
                # doc_qa_prompt = DOC_QA_PROMPT_TEMPLATE.format(
                #     doc_content=doc_raw_content, question=query
                # )

                doc_qa_prompt = langfuse.get_prompt(DOC_QA_PROMPT_TEMPLATE_NAME).compile(
                    doc_content=doc_raw_content, question=query
                )
                return self.streaming_llm_output(
                    query=doc_qa_prompt,
                    chat_history=chat_history,
                    related_docs=related_chunks,
                    original_query=original_query,
                )

            else:
                doc = related_docs[0]
                content = (
                    doc.get("answer_markdown")
                    if doc.get("answer_markdown")
                    else doc.get("answer")
                )
                return self.streaming_simu_output(
                    query=original_query,
                    content=content,
                    chat_history=chat_history,
                    related_docs=related_docs,
                )

        if not chat_history:
            return retrieve_and_rag(query=query, original_query=query)

        """
        # 判断是否跨意图
        1.如果有跨意图
        表明当前的问题是一个新的问题，就不拼接历史对话，直接用当前问题进行作答
        
        2.如果没有跨意图
        表明当前的问题和前面的问题还在一个意图下，就拼接历史对话，根据历史对话问题，重写一个问题，再进行作答
        """

        dialog_content = self.dialog_format(query, chat_history)
        # cross_intent_prompt = ACROSS_INTENT_PROMPT.format(context=dialog_content)
        cross_intent_prompt = langfuse.get_prompt(ACROSS_INTENT_PROMPT_NAME).compile(context=dialog_content)
        is_cross_intent = (
            post_api_for_llm(
                content=cross_intent_prompt,
                trace_id=trace_id,
                user_id=user_id,
                session_id=session_id,
                module_name=f"{module_name}-cross-intent"
            )
            == GradeScore.YES
        )

        if is_cross_intent:
            return retrieve_and_rag(
                query=query, chat_history=chat_history, original_query=query
            )
        else:
            # 问题重写
            rewrite_question_content = self.rewrite_format(query, chat_history)
            # logger.info(f"rewrite_question_content: {rewrite_question_content}")
            rewrite_question = post_api_for_llm(content=rewrite_question_content,
                                                trace_id=trace_id,
                                                user_id=user_id,
                                                session_id=session_id,
                                                module_name=f"{module_name}-rewrite-question"
                                                )
            return retrieve_and_rag(
                query=rewrite_question, chat_history=chat_history, original_query=query
            )


if __name__ == "__main__":
    local_hybrid_rag = LocalHybridRag()
    # query = "北京地区的呢?"
    query = "我想要请产假怎么处理?"
    # chat_history = [
    #     {"role": "user", "content": "育儿假怎么休"},
    #     {
    #         "role": "assistant",
    #         "content": "育儿假的请休按周年计算,即以子女周岁作为计算年度.",
    #     },
    #     {"role": "user", "content": "湖南地区的"},
    #     {
    #         "role": "assistant",
    #         "content": "湖南地区的育儿假规定按周年计算，以子女周岁作为计算年度，满2年则递进计算",
    #     },
    # ]

    query = "出差杭州的差旅标准"
    query = "出差杭州的住宿标准"
    query = "怎么申请年休假，有哪些规定？"
    chat_history = []

    import time

    start = time.time()

    query = "杭州出差标准呢"

    chat_history = [
        {"role": "user", "content": "出差补助是多少"},
        {
            "role": "assistant",
            "content": "这个问题暂时未覆盖，数字员工还在学习升级中，敬请期待~可以先问我其他问题试试哦！",
        },
        {"role": "user", "content": "北京出差补助"},
        {
            "role": "assistant",
            "content": "北京出差的补助标准为每人每天100元，包含伙食和交通补助。这一标准适用于所有级别的员工。需要注意的是，公司助理总经理级及以上成员的住宿可安排单间，其住宿费标准为650元/人/天，部门助理总监/资深及以上人员为550元/人/天，其他人员为450元/人/天。这些费用标准和补助旨在覆盖出差期间的基本生活和交通需求，确保员工在出差期间能够得到合理的支持。",
        },
    ]

    query = "出差南昌的报销标准"
    query = "南昌差旅标准"
    query = "杭州出差差旅费标准"
    chat_history = [
        {"role": "user","content": "美欧"}
    ]

    # query = "出差上海报销标准"
    # chat_history = [
    #     {"role": "user", "content": "出差南昌报销标准"},
    #     {
    #         "role": "assistant",
    #         "content": "这个问题暂时未覆盖，数字员工还在学习升级中，敬请期待~可以先问我其他问题试试哦！",
    #     },
    #     {"role": "user", "content": "出差上海报销标准"},
    #     {
    #         "role": "assistant",
    #         "content": "出差上海的报销标准如下：1.住宿费 1.公司助理总经理及以上成员：600元、部门助理总监及以上成员：500元、其他人员：400元；2.交通费用：100元/人/天；3.餐费：100元/人/天；4.其他费用：100元/人/天。以上费用标准适用于出差期间的基本生活和交通需求，确保员工在出差期间能够得到合理的支持。",
    #     },
    #     {"role": "user", "content": "我是资深员工"},
    #     {
    #         "role": "assistant",
    #         "content": "资深员工的出差报销标准如下：1.乘坐交通工具： 1.飞机：经济舱 2.高铁：二等座 3.火车：硬卧 4.轮船：三等舱 ",
    #     },
    # ]

    for resp, history in local_hybrid_rag.dialog_onetune(query, chat_history):
        # print(resp, history)
        print("------------------------", resp, history)
    # print(time.time() - start)
