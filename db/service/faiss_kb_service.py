import sys

sys.path.append("./")

import os
import shutil
from typing import List, Dict, Optional
from functools import lru_cache

from langchain.docstore.document import Document

from configs.model_config import (
    VECTOR_SEARCH_SCORE_THRESHOLD,
    KB_ROOT_PATH,
    CACHED_VS_NUM,
    VECTOR_SEARCH_TOP_K,
)
from db.embedding_utils import embed_model

from vectorstores import MyFAISS, MyCustomFAISS
from db.service.base import KBService, SupportedVSType
from utils import torch_gc


def get_doc_path(knowledge_base_name: str):
    """获取上传的源文件文件夹"""
    return os.path.join(KB_ROOT_PATH, knowledge_base_name, "content")


def get_kb_path(knowledge_base_name: str):
    """获取向量索引库根路径"""
    return os.path.join(KB_ROOT_PATH, knowledge_base_name)


def get_vs_path(knowledge_base_name: str):
    """获取faiss索引文件路径"""
    return os.path.join(KB_ROOT_PATH, knowledge_base_name, "vector_store")


def get_file_path(knowledge_base_name: str, doc_name: str):
    """获取文件路径"""
    return os.path.join(KB_ROOT_PATH, knowledge_base_name, "content", doc_name)


def list_kbs_from_folder():
    return [
        f
        for f in os.listdir(KB_ROOT_PATH)
        if os.path.isdir(os.path.join(KB_ROOT_PATH, f))
    ]


@lru_cache(CACHED_VS_NUM)
def load_vector_store(vs_path, embeddings=embed_model):
    return MyCustomFAISS.load_local(vs_path, embeddings)


class FaissKBService(KBService):
    vs_path: str
    vector_name: str = None
    vector_store: None
    # _index_to_docstore_id: Dict = {}
    # _docstore_id_to_index: Dict = {}
    _docstore_id_to_document: Dict = {}

    def __init__(
        self, knowledge_base_name, embed_model: str = ..., docs: List[Document] = None
    ):
        super().__init__(knowledge_base_name, embed_model)
        if knowledge_base_name not in list_kbs_from_folder():
            self.do_create_kb(docs)
        self.load_vector_store()

    @property
    def vs_type(self) -> str:
        return SupportedVSType.FAISS

    def get_vs_path(self):
        return get_vs_path(knowledge_base_name=self.kb_name)

    def load_vector_store(self):
        self.vector_store = load_vector_store(self.get_vs_path())
        # self._index_to_docstore_id = self.vector_store.index_to_docstore_id
        # self._docstore_id_to_document = self.vector_store.docstore._dict
        self._knowledge_id_to_document = {
            v.metadata.get("knowledge_id"): {"index_id": k, "doc": v}
            for k, v in self.vector_store.docstore._dict.items()
            if v.metadata.get("knowledge_id")
        }

        return self.vector_store

    def save_vector_store(self):
        self.vector_store.save_local(self.get_vs_path())

    def get_doc_by_id(self, id: str):
        # return self._docstore_id_to_document.get(id)
        return self._knowledge_id_to_document.get(id)

    def kb_exists(self):
        return os.path.exists(self.get_vs_path())

    def do_create_kb(self, docs: List[Document] = None):
        if not docs:
            pass
        self.vector_store = MyCustomFAISS.from_documents(docs, embed_model)
        torch_gc()
        self.vector_store.save_local(self.get_vs_path())

    def do_add_doc(self, docs: List[Document]) -> List[Dict]:
        ids = self.vector_store.add_documents(docs)
        # 添加到全局变量中
        for id, doc in zip(ids, docs):
            knowledge_id = doc.metadata.get("knowledge_id")
            if not knowledge_id:
                continue
            self._knowledge_id_to_document.setdefault(
                knowledge_id, {"index_id": id, "doc": doc}
            )
        # 持久化
        self.vector_store.save_local(self.get_vs_path())
        return ids

    def do_update_doc(self, docs: List[Document] = None):
        ids = []
        for doc in docs:
            knowledge_id = doc.get("knowledge_id")
            if not knowledge_id:
                continue
            ids.append(knowledge_id)
        self.do_delete_doc(ids=ids)

        new_docs = []
        for doc in docs:
            question = doc["question"]
            metadata = doc
            metadata.pop("question")
            p = Document(page_content=question, metadata=metadata)
            new_docs.append(p)
        ids = self.do_add_doc(docs=new_docs)
        self.vector_store.save_local(self.get_vs_path())

    def do_delete_kb(self):
        try:
            shutil.rmtree(get_kb_path(knowledge_base_name=self.kb_name))
            self.vector_store = None
            self._knowledge_id_to_document = {}
        except Exception as e:
            print(e)

    def do_search(
        self, query: str, topk: int = VECTOR_SEARCH_TOP_K, score_threshold: float = None
    ):
        return self.vector_store.similarity_search_with_score(query, topk=topk)

    def delete_doc(self, ids: List[str] = None):
        self.do_delete_doc(ids=ids)

    def do_delete_doc(self, ids: List[str] = None):
        """ids是knowledge_ids，对应数据库中的ids,映射到faiss的uuid"""
        index_ids = [
            self._knowledge_id_to_document[_id]["index_id"]
            for _id in ids
            if _id in self._knowledge_id_to_document
        ]
        self.vector_store.delete(index_ids)
        for _id in ids:
            if _id in self._knowledge_id_to_document:
                self._knowledge_id_to_document.pop(_id)
        # 持久化
        self.vector_store.save_local(self.get_vs_path())


if __name__ == "__main__":
    kbs = list_kbs_from_folder()
    print(kbs)

    q = "你是谁"
    a = "我是小天"
    from datetime import datetime

    d1 = Document(
        page_content=q,
        metadata={"content": a, "knowledge_id": 1, "time": datetime.now()},
    )
    faiss_index_kb = FaissKBService(knowledge_base_name="test_ss", docs=[d1])

    # TODO: 测试
    # 添加文档
    # ids = faiss_index_kb.add_doc([d1])
    # print(ids)

    # 删除文档
    ids = [1]
    faiss_index_kb.delete_doc(ids=ids)

    # 更新文档
    # d2 = {
    #     "knowledge_id": 1,
    #     'question': q,
    #     'content': a,
    #     'age': 19,
    #     'time': datetime.now()
    # }
    # faiss_index_kb.update_doc([d2])

    # 查询文档
    # recalls = faiss_index_kb.do_search("你是谁呀")
    # print(recalls)
