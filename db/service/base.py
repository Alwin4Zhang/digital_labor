import os
from abc import ABC, abstractmethod
from typing import List, Union, Dict, Optional

import numpy as np
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document

from configs.model_config import EMBEDDING_MODEL, VECTOR_SEARCH_TOP_K

from db.dao.knowledge_base_dao import (
    add_qa_to_db,
    add_document_to_db,
    delete_qa_from_db,
    update_qa_by_id,
    get_qa_detail,
    list_qas_from_db,
)
from db.dao.dialogue_history_dao import (
    add_dialogue_history_to_db,
    get_dialogue_history_by_id,
    filter_dialogue_history,
)

from db.embedding_utils import embed_documents_api


def normalize(embeddings: List[List[float]]) -> np.ndarray:
    """
    sklearn.preprocessing.normalize 的替代（使用 L2），避免安装 scipy, scikit-learn
    """
    norm = np.linalg.norm(embeddings, axis=1)
    norm = np.reshape(norm, (norm.shape[0], 1))
    norm = np.tile(norm, (1, len(embeddings[0])))
    return np.divide(embeddings, norm)


class SupportedVSType:
    FAISS = "faiss"
    MILVUS = "milvus"
    ES = "es"
    # TODO
    # DEFAULT = 'default'
    # ZILLIZ = 'zilliz'
    # PG = 'pg'


class KBService(ABC):

    def __init__(self, knowledge_base_name, embed_model: str = EMBEDDING_MODEL):
        self.kb_name = knowledge_base_name
        self.embed_model = embed_model

    def __repr__(self) -> str:
        return f"{self.kb_name} @ {self.embed_model}"

    @abstractmethod
    def kb_exists(self):
        """检查知识库是否已经存在"""
        pass

    def save_vector_store(self):
        """保存向量库:FAISS保存到磁盘，milvus保存到数据，PGVector TODO:"""
        pass

    def create_kb(self):
        """创建知识库"""
        if not self.kb_exists():
            self.do_create_kb()

    def delete_kb(self):
        """删除知识库"""
        if self.kb_exists():
            self.do_delete_kb()

    @abstractmethod
    def do_delete_kb(self):
        pass

    @abstractmethod
    def do_create_kb(self, docs: List[Document] = None):
        """创建知识库"""
        pass

    def _docs_to_embeddings(self, docs: List[Document]) -> Dict:
        """
        将 List[Document] 转化为 VectorStore.add_embeddings 可以接受的参数
        """
        return embed_documents_api(docs=docs)

    @abstractmethod
    def do_search(
        self, query: str, topk: int = VECTOR_SEARCH_TOP_K, score_threshold: float = None
    ):
        """向量库检索，子类需实现"""
        pass

    def add_doc(self, docs: List[dict] = None, **kwargs):
        """向索引库添加知识"""
        # for doc in docs:
        #     doc.metadata.setdefault("kb_name", self.kb_name)
        return self.do_add_doc(docs=docs, **kwargs)

    def update_doc(self, docs: List[dict] = None, **kwargs):
        return self.do_update_doc(docs=docs, **kwargs)

    @abstractmethod
    def do_update_doc(self, docs: List[dict] = None):
        pass

    def delete_doc(self, docs: List[dict] = None):
        # ids = [doc.get(field) for doc in docs if doc.get(field)]
        # self.do_delete_doc(ids=ids)
        pass

    @abstractmethod
    def do_add_doc(
        self,
        docs: List[dict],
    ) -> List[Dict]:
        """向索引库添加文档，子类需实现"""
        pass

    @abstractmethod
    def do_delete_doc(self, ids: List[str] = None):
        """索引库删除，子类需实现"""
        pass

    def query_compare_by_score(
        self,
        q1: str,
        q2: str,
        topk: int = VECTOR_SEARCH_TOP_K,
        score_threshold: float = None,
    ):
        """根据传入的q1,q2判断哪个q更接近知识库"""
        docs1 = self.do_search(q1, topk=topk, score_threshold=score_threshold)
        docs2 = self.do_search(q2, topk=topk, score_threshold=score_threshold)

        if not docs1 and not docs2:  # q1,q2都没有相似
            return 2, []
        if not docs1 and docs2:  # q1没有相似，q2相似
            return 0, docs2
        if docs1 and not docs2:  # q1相似，q2没有相似
            return 1, docs1
        if docs1 and docs2:  # q1,q2都有相似
            distance1, distance2 = docs1[0]["distance"], docs2[0]["distance"]
            if distance1 <= distance2:
                return 1, docs1
        return 0, docs2


class KBServiceFactory:

    @staticmethod
    def get_service(
        kb_name: str,
        vector_store_type: str,
        embed_model: str = EMBEDDING_MODEL,
        docs: List[Document] = None,
    ):
        if isinstance(vector_store_type, str):
            vector_store_type = getattr(SupportedVSType, vector_store_type.upper())
        if vector_store_type == SupportedVSType.FAISS:
            from db.service.faiss_kb_service import FaissKBService

            return FaissKBService(knowledge_base_name=kb_name)
        if vector_store_type == SupportedVSType.MILVUS:
            from db.service.milvus_kb_service import MilvusKBService

            return MilvusKBService(knowledge_base_name=kb_name)
        if vector_store_type == SupportedVSType.ES:
            from db.service.elasticsearch_kb_service import ElasticsearchKBService

            return ElasticsearchKBService(knowledge_base_name=kb_name)
        # if vector_store_type == SupportedVSType.PG:
        #     pass

    @staticmethod
    def get_default():
        return KBServiceFactory.get_service("default", SupportedVSType.FAISS)
