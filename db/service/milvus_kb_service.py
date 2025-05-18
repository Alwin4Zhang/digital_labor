import sys

sys.path.append("./")
from typing import List, Dict, Optional

import numpy as np
from langchain.schema import Document
from langchain.vectorstores.milvus import Milvus

from pymilvus import MilvusClient
from pymilvus import utility, connections, Collection
from pymilvus import FieldSchema, CollectionSchema, DataType

from configs.apollo_config import (
    MILVUS_HOST,
    MILVUS_PORT,
    MILVUS_USERNAME,
    MILVUS_PASSWORD,
)
from configs.model_config import VECTOR_SEARCH_TOP_K
from configs.apollo_config import DEFAULT_MILVUS_KB_NAME

from db.service.base import KBService, SupportedVSType

# from db.embedding_utils import embed_model, embed_texts, embed_documents
from db.embedding_utils import embed_texts_api, embed_documents_api
from utils.common import timeit
from configs.apollo_config import logger


class MilvusKBService(KBService):
    # milvus: MilvusClient
    # vector_store: None
    dim: int = 1024

    def __init__(self, knowledge_base_name, embed_model: str = ...):
        super().__init__(knowledge_base_name, embed_model)
        self._init_db_connection()

    def _init_db_connection(self):
        # 创建连接
        self.milvus = MilvusClient(
            uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}",
            user=MILVUS_USERNAME,
            password=MILVUS_PASSWORD,
        )
        self.do_create_kb()

    @staticmethod
    def get_collection(milvus_name):
        return Collection(milvus_name)

    def get_doc_by_id(
        self, ids: List[str], release_status: str = None
    ) -> Optional[Document]:
        """根据konwledge_id返回查询文档"""
        _filter = f"knowledge_id in {ids}"
        if release_status:
            _filter += f" and release_status == '{release_status}'"
        docs = self.milvus.query(
            self.kb_name,
            filter=_filter,
            output_fields=["question", "answer", "knowledge_id", "release_status"],
        )
        return docs

    def do_create_kb(self, docs: List[Document] = None, metric_type="IP"):
        has = self.kb_exists()
        print(f"Does collection {self.kb_name} exist in Milvus: {has}")
        if has:
            # self.do_delete_kb()
            return self.milvus
        self.milvus.create_collection(
            collection_name=self.kb_name,
            dimension=self.dim,
            consistency_level="Bounded",
            metric_type=metric_type,
            auto_id=True,
        )
        print("collections:", self.milvus.list_collections())
        print(f"{self.kb_name} :", self.milvus.describe_collection(self.kb_name))

    @property
    def vs_type(self) -> str:
        return SupportedVSType.MILVUS

    def kb_exists(self):
        """查询是否已存在"""
        return self.kb_name in self.milvus.list_collections()

    def do_delete_kb(self):
        if self.kb_exists():
            self.milvus.drop_collection(self.kb_name)

    @timeit
    def do_search(
        self,
        query: str = None,
        topk: int = VECTOR_SEARCH_TOP_K,
        score_threshold: float = None,
        release_status: str = None,
        append_fields: List[str] = None,
        query_vector: List[float] = None,
    ):
        # embeddings = embed_texts([query])
        embeddings = query_vector if query_vector else embed_texts_api(query)
        search_params = {
            "metric_type": "IP",  # "L2"
            "offset": 0,
            "ignore_growing": False,
            "params": {
                "nprobe": 10,
                "radius": score_threshold,
                # filter out most similar vectors with a distance greater than or equal to 1.0
                "range_filter": 1.0,
            },
        }

        _filter = None
        if release_status:
            _filter = f"release_status == '{release_status}'"
        output_fields = [
            "question",
            "answer",
            "chunk_index",
            "knowledge_id",
            "release_status",
            "document_uuid",
            "filename",
        ]
        if append_fields:
            if isinstance(append_fields, str):
                append_fields = [append_fields]
            output_fields.extend(append_fields)
        result = self.milvus.search(
            self.kb_name,
            embeddings,
            search_params=search_params,
            limit=topk,
            filter=_filter,
            output_fields=output_fields,
        )
        docs = [hit for hits in result for hit in hits]
        if score_threshold:
            docs = [doc for doc in docs if doc["distance"] >= score_threshold]
        for doc in docs:
            doc["entity"].update(
                {
                    "distance": doc["distance"],
                    "id": doc["id"],
                }
            )
            if "chunk_index" in doc["entity"]:
                doc["entity"]["chunk_id"] = int(doc["entity"]["chunk_index"])
                doc["entity"].pop("chunk_index")
        return [doc["entity"] for doc in docs]

    @timeit
    def do_add_doc(self, docs: List[dict]) -> List[str]:
        qs = []
        rest_docs = []
        for i, doc in enumerate(docs):
            q = doc.get("question")
            if not q:
                continue
            qs.append(q)
            rest_docs.append(doc)
        qvs = np.array(embed_texts_api(qs))
        for i, doc in enumerate(rest_docs):
            rest_docs[i]["vector"] = qvs[i]
        docs = rest_docs
        pks = self.milvus.insert(self.kb_name, docs, progress_bar=True)
        return pks

    def delete_doc(self, docs: List[dict] = None, field="knowledge_id"):
        ids = [doc.get(field) for doc in docs if doc.get(field)]
        return self.do_delete_doc(ids=ids)

    def do_delete_doc(self, ids: List[str] = None) -> List[str]:
        """根据ids删除对应的索引"""
        print(f"knowledge_id in {ids}")
        docs = self.milvus.query(
            self.kb_name,
            filter=f"knowledge_id in {ids}",
            output_fields=["knowledge_id"],
        )
        ids = [doc["id"] for doc in docs]
        if ids:
            return self.milvus.delete(self.kb_name, pks=ids, progress_bar=True)
        return []

    def do_update_doc(self, docs: List[dict]) -> List[str]:
        # 先删除后添加
        # ids = [doc['knowledge_id'] for doc in docs]
        # self.do_delete_doc(ids)
        self.delete_doc(docs=docs)
        pks = self.do_add_doc(docs)
        return pks


default_vector_db = MilvusKBService(knowledge_base_name=DEFAULT_MILVUS_KB_NAME)

if __name__ == "__main__":
    # pass
    # milvus_index_kb = MilvusKBService(knowledge_base_name='test_rb')

    # print(milvus_index_kb.kb_exists())

    q = "你是谁"
    a = "我是小天"
    import numpy as np

    # # print(np.array(embed_texts(q)[0]).shape)
    # d1 = {
    #     'knowledge_id': 1,
    #     "question": q,
    #     "answer": a,
    #     "release_status": "released",
    #     "vector": np.array(embed_texts([q])[0])
    # }

    # # # print(d1)

    # # 创建kb
    # milvus_index_kb.do_create_kb()
    # # 插入数据

    # q = "你今天去哪里?"
    # a = "我要去北京"
    # # print(np.array(embed_texts([q])[0]).shape)
    # d2 = {
    #     'knowledge_id': 2,
    #     "question": q,
    #     "answer": a,
    #     "release_status": "await",
    #     "vector": np.array(embed_texts(q)[0])
    # }

    # q = "今天天气不错"
    # a = "是吗？我没有发现呢"
    # d3 = {
    #     'knowledge_id': 3,
    #     "question": q,
    #     "answer": a,
    #     "release_status": "released",
    #     "vector": np.array(embed_texts(q)[0])
    # }

    # pks = milvus_index_kb.do_add_doc([d1, d2, d3])
    # print(pks)

    # 查询数据
    # docs = milvus_index_kb.do_search(query='你是谁')
    # print(docs)

    # # # 更新数据
    # d3 = {
    #     'knowledge_id': 2,
    #     "question": q + "123",
    #     "answer": a + "123",
    #     "vector": np.array(embed_texts(q)[0])
    # }

    # d4 = {
    #     'knowledge_id': 1,
    #     "question": q + "123",
    #     "answer": a + "123",
    #     "vector": np.array(embed_texts(q)[0])
    # }
    # # milvus_index_kb.do_update_doc([d3])
    # milvus_index_kb.update_doc([d3, d4])

    # # 删除数据
    # print('-------', milvus_index_kb.do_delete_doc(ids=[1, 2, 3]))

    docs = default_vector_db.do_search(query="你是谁")
    print(docs)

    # docs = milvus_index_kb.do_search(query='你是谁')
    # print(docs)

    # get doc by id
    # docs = milvus_index_kb.get_doc_by_id(ids=['1', '2'])
    # print(docs)
