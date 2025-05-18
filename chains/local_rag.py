import sys
import re
import time
import copy

sys.path.append("./")

import datetime
from typing import List
from functools import lru_cache
from abc import ABC, abstractmethod

import numpy as np
from tqdm import tqdm

# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from fuzzywuzzy import fuzz

from configs.model_config import *
from configs.constants import special_question_dict

# from db.dao.dialogue_history_dao import add_dialogue_history_to_db as create_dialog
from db.service.milvus_kb_service import default_vector_db
from db.service.elasticsearch_kb_service import default_es_db
from utils.llm_util import post_api_for_llm, apost_api_for_llm
from utils.common import thread_parallel

URL_REG = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
MODEL_PROMPT_TEMPLATE = CHATGLM_PROMPT_TEMPLATE


# patch HuggingFaceEmbeddings to make it hashable
# def _embeddings_hash(self):
#     return hash(self.model_name)


# HuggingFaceEmbeddings.__hash__ = _embeddings_hash


def generate_prompt(
    related_docs: List[str],
    prompt_template: str = CHATGLM_PROMPT_TEMPLATE,
) -> str:
    """构建LLM的prompt"""
    context = "\n".join([doc.page_content for doc in related_docs])
    prompt = prompt_template.replace("{context}", context)
    return prompt


# def search_multimodal_content(related_docs: List[str]):
#     """验证相关答案中是否有多模态的内容：如网址链接，图片，table标签等
#     Args:
#         related_docs (List[str]): 召回的相关的文档
#     """
#     if not related_docs:
#         return False
#     related_docs_contents = [doc.page_content for doc in related_docs]
#     # TODO:目前取-1有问题，需要重构
#     most_similar_content = related_docs_contents[-1]
#     if re.search(r'<(img|table).*>', most_similar_content):
#         return True
#     return False


def search_multimodal_content(content: str):
    """验证相关答案中是否有多模态的内容：如网址链接，图片，table标签等
    Args:
        content (str): 召回的内容
    """
    if not content:
        return False
    if re.search(r"<(img|table).*>", content):
        return True
    return False


class LocalRAG(object):

    top_k = VECTOR_SEARCH_TOP_K
    score_threshold = VECTOR_SEARCH_SCORE_THRESHOLD

    def __init__(self) -> None:
        pass

    def multi_query_retrieve(self, history):
        """当前问题检索不到结果时，使用多轮的问题拼接后检索,兼容history是tuple or json不同的格式"""
        context = ""
        for i, h in enumerate(history):
            if isinstance(h[0], dict):
                context += " " + h[0]["content"]
            elif isinstance(h[0], tuple):
                context += " " + h[0]
        return context

    def history_format(self, history):
        """转换history格式"""
        res = []
        for i, h in enumerate(history):
            if isinstance(h[0], dict):
                return history
            elif isinstance(h, (tuple, list)):
                res.append(
                    [
                        {"role": "user", "type": "input", "content": h[0]},
                        {"role": "assistant", "type": "llm", "content": h[1]},
                    ]
                )
        return res

    def streaming_simu_output(
        self,
        query,
        content,
        chat_history=None,
        interval=0.05,
        limit=500,
        related_docs=None,
        force_type="retrieve",
        is_append: bool = False,
        use_retell=False,
    ):
        """检索到模拟流式输出"""
        origin_chat_history = copy.deepcopy(chat_history)
        chat_history = (chat_history + [[]]) if chat_history else [[]]
        wait = False
        if len(content) <= limit:
            wait = True
        if not use_retell:  # 不使用复述
            resp = ""
            for i, token in enumerate(content):
                if wait:
                    time.sleep(interval)
                resp += token
                if i <= 5:
                    resp = resp.lstrip()
                chat_history[-1] = [
                    {"role": "user", "type": "input", "content": query},
                    {"role": "assistant", "type": force_type, "content": resp},
                ]
                chat_history[-1][0]["content"] = query
                response = {
                    "knowledge_id": (
                        related_docs[0]["knowledge_id"] if related_docs else None
                    ),
                    "query": query,
                    "result": token if not is_append else resp,
                    "type": force_type,
                    "source_documents": related_docs,
                }
                yield response, chat_history
        else:
            # 检索content内容，如果有html标签，则原样返回，不做处理
            has_html_tag = search_multimodal_content(content)
            if has_html_tag or force_type == "llm":
                resp = ""
                for i, token in enumerate(content):
                    if wait:
                        time.sleep(interval)
                    resp += token
                    chat_history[-1] = [
                        {"role": "user", "type": "input", "content": query},
                        {"role": "assistant", "type": force_type, "content": resp},
                    ]
                    chat_history[-1][0]["content"] = query
                    response = {
                        "knowledge_id": (
                            related_docs[0]["knowledge_id"] if related_docs else None
                        ),
                        "query": query,
                        "result": token if not is_append else resp,
                        "type": force_type,
                        "source_documents": related_docs,
                    }
                    yield response, chat_history
            else:
                # 重述
                for response, chat_history in self.streaming_simu_retell_output(
                    query,
                    content,
                    chat_history=origin_chat_history,
                    related_docs=related_docs,
                    force_type=force_type,
                    is_append=is_append,
                ):
                    yield response, chat_history

    def streaming_simu_retell_output(
        self,
        query,
        content,
        chat_history=None,
        related_docs=None,
        force_type="retrieve",
        is_append: bool = False,
    ):
        """检索到用大模型润色后输出"""
        if chat_history is None:
            chat_history = []
        stream_resp = ""
        current_history = []
        for h in chat_history:
            current_history.append(h[0])
            current_history.append(h[1])
        chat_history = (chat_history + [[]]) if chat_history else [[]]
        retell_prompt = CHATGLM3_RETELL_PROMPT_TEMPLATE.format(
            question=query, answer=content
        )
        for inum, chunk in enumerate(
            apost_api_for_llm(content=retell_prompt, history=current_history)
        ):
            choice = chunk["choices"][0]["delta"]
            content = choice["content"]
            if inum <= 5:
                content = content.lstrip()
            stream_resp += content
            chat_history[-1] = [
                {
                    "role": "user",
                    "type": "input",
                    "content": query,
                },
                {"role": "assistant", "type": "llm", "content": stream_resp},
            ]

            response = {
                "knowledge_id": (
                    related_docs[0]["knowledge_id"] if related_docs else None
                ),
                "query": query,
                "result": content if not is_append else stream_resp,
                "type": force_type,
                "source_documents": related_docs,
            }

            yield response, chat_history

    def streaming_llm_output(
        self,
        query,
        chat_history=None,
        related_docs=None,
        origin_q=None,  # 支持自定义prompt,
        is_append: bool = False,
    ):
        if chat_history is None:
            chat_history = []
        stream_resp = ""
        current_history = []
        for h in chat_history:
            current_history.append(h[0])
            current_history.append(h[1])

        chat_history = (chat_history + [[]]) if chat_history else [[]]
        for inum, chunk in enumerate(
            apost_api_for_llm(content=query, history=current_history)
        ):
            choice = chunk["choices"][0]["delta"]
            content = choice["content"]
            if inum <= 5:
                content = content.lstrip()
            stream_resp += content
            chat_history[-1] = [
                {
                    "role": "user",
                    "type": "input",
                    "content": query,
                },
                {"role": "assistant", "type": "llm", "content": stream_resp},
            ]
            if origin_q:
                query = origin_q

            response = {
                "query": query,
                "result": content if not is_append else stream_resp,
                "type": "llm",
                "source_documents": related_docs,
            }
            yield response, chat_history

    def dialog_onetune(self, query, chat_history=None, is_append: bool = False):
        if chat_history:
            chat_history = self.history_format(chat_history)
        if not chat_history:
            related_docs = default_vector_db.do_search(
                query=query,
                topk=self.top_k,
                score_threshold=self.score_threshold,
                release_status="released",
            )
            if not related_docs:
                return self.streaming_llm_output(
                    query,
                    chat_history=chat_history[:],
                    related_docs=[],
                    is_append=is_append,
                )
            else:
                doc = related_docs[0]
                question = doc.get("question")
                content = doc.get("answer")
                if (
                    question in special_question_dict
                ):  # 特殊的问题走prompt提示原样输出，比如自我认知
                    return self.streaming_simu_output(
                        query,
                        content,
                        related_docs=[],
                        force_type="llm",
                        is_append=is_append,
                    )
                related_documents = [i for i in related_docs if i.get("question")]
                return self.streaming_simu_output(
                    query, content, related_docs=related_documents, is_append=is_append
                )

        last_questions = []
        last_answers = []
        for i in range(len(chat_history) - 1, -1, -1):
            last_question = chat_history[i][0]["content"]
            last_answer = chat_history[i][-1]["content"]
            last_questions.append(last_question)
            last_answers.append(last_answer)
            tquery = self.multi_query_retrieve(chat_history[i:]) + " " + query
            # 判断当前组合的问题和当前问题哪个相似度高
            flag, related_docs = default_vector_db.query_compare_by_score(
                q1=query, q2=tquery, score_threshold=self.score_threshold
            )
            related_documents = [
                i for i in related_docs if i.get("question")
            ]  # 相关的用于展示的相关链接
            if flag == 1:
                q = related_docs[0]["question"]
                a = related_docs[0]["answer"]
                # chat_history += [[]]
                if (
                    q in special_question_dict
                ):  # 特殊的问题走prompt提示原样输出，比如自我认知
                    return self.streaming_simu_output(
                        query,
                        content=a,
                        chat_history=chat_history[:],
                        related_docs=[],
                        force_type="llm",
                        is_append=is_append,
                    )

                return self.streaming_simu_output(
                    query,
                    content=a,
                    chat_history=chat_history[:],
                    related_docs=related_documents,
                    is_append=is_append,
                )
            elif flag == 2:
                return self.streaming_llm_output(
                    query,
                    chat_history=chat_history[:],
                    related_docs=related_documents,
                    is_append=is_append,
                )
            if related_docs:  # 拼接后的query召回

                q = related_docs[0]["question"]
                a = related_docs[0]["answer"]
                if a in last_answers:
                    related_docs = default_vector_db.do_search(
                        query, topk=self.top_k, score_threshold=self.score_threshold
                    )
                    related_documents = [i for i in related_docs if i.get("question")]
                    if related_docs:
                        q = related_docs[0]["question"]
                        ta = related_docs[0]["answer"]
                        # chat_history += [[]]
                        if (
                            q in special_question_dict
                        ):  # 特殊的问题走prompt提示原样输出，比如自我认知
                            return self.streaming_simu_output(
                                query,
                                content=ta,
                                chat_history=chat_history[:],
                                related_docs=[],
                                force_type="llm",
                                is_append=is_append,
                            )
                        return self.streaming_simu_output(
                            query,
                            content=ta,
                            chat_history=chat_history[:],
                            related_docs=related_documents,
                            is_append=is_append,
                        )
                    else:
                        return self.streaming_llm_output(
                            query,
                            chat_history=chat_history[:],
                            related_docs=related_documents,
                            is_append=is_append,
                        )
                else:
                    # chat_history += [[]]
                    if (
                        q in special_question_dict
                    ):  # 特殊的问题走prompt提示原样输出，比如自我认知
                        return self.streaming_simu_output(
                            query,
                            content=a,
                            chat_history=chat_history[:],
                            related_docs=[],
                            force_type="llm",
                            is_append=is_append,
                        )
                    return self.streaming_simu_output(
                        query,
                        content=a,
                        chat_history=chat_history[:],
                        related_docs=related_documents,
                        is_append=is_append,
                    )
            else:
                related_docs = default_vector_db.do_search(
                    query, topk=self.top_k, score_threshold=self.score_threshold
                )
                related_documents = [i for i in related_docs if i.get("question")]
                if related_docs:
                    q = related_docs[0]["question"]
                    ta = related_docs[0]["answer"]
                    # chat_history += [[]]
                    if (
                        q in special_question_dict
                    ):  # 特殊的问题走prompt提示原样输出，比如自我认知
                        return self.streaming_simu_output(
                            query,
                            content=ta,
                            chat_history=chat_history,
                            related_docs=[],
                            force_type="llm",
                            is_append=is_append,
                        )
                    return self.streaming_simu_output(
                        query,
                        content=ta,
                        chat_history=chat_history,
                        related_docs=related_documents,
                        is_append=is_append,
                    )
                else:
                    return self.streaming_llm_output(
                        query,
                        chat_history=chat_history,
                        related_docs=related_documents,
                        is_append=is_append,
                    )

    def get_knowledge_based_answer_multi_round(
        self, query, chat_history=None, is_append: bool = False
    ):
        """
        多轮对话覆盖
        """
        return self.dialog_onetune(
            query, chat_history=chat_history, is_append=is_append
        )

    def question_validate(self, question, threshold=90):
        res = []
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
        candidates = [(hit["_id"], hit["_source"]["question"]) for hit in hits]

        for _id, cand in candidates:
            simi = fuzz.ratio(question, cand)
            if simi >= threshold:
                res.append((_id, cand, simi))
        return res

    def question_validate_parallel(self, questions, threshold=90):
        '''batch question validate'''
        
        def do_search(i, question, dsl):
            res = []
            hits = default_es_db.do_search(question, dsl=dsl)
            candidates = [(hit["_id"], hit["_source"]["question"]) for hit in hits]
            
            for _id, cand in candidates:
                simi = fuzz.ratio(question, cand)
                if simi >= threshold:
                    res.append((_id, cand, simi))
            return i,question,res
        

        args_list = []
        for i, question in enumerate(questions):
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
            args_list.append((i, question, dsl))

        
        return thread_parallel(do_search, args_list)
