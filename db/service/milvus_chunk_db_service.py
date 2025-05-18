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
    DEFAULT_MILVUS_CHUNK_DB_NAME
)
from configs.model_config import (
    VECTOR_SEARCH_TOP_K,
    CHUNK_VECTOR_SEARCH_SCORE_THRESHOLD,
)

# from db.service.base import KBService, SupportedVSType
from db.service.milvus_kb_service import MilvusKBService
from db.embedding_utils import embed_texts_api, embed_documents_api
from utils.common import timeit
from utils.llm_util import get_num_tokens_from_messages


class MilvusChunkDBService(MilvusKBService):
    # milvus: MilvusClient
    # vector_store: None
    dim: int = 1024
    kb_name: str = DEFAULT_MILVUS_CHUNK_DB_NAME
    score_threshold: float = CHUNK_VECTOR_SEARCH_SCORE_THRESHOLD
    metric_type: str = "IP"
    MAX_CHUNK_LEN = 65535  # 最大chunk长度

    def _init_db_connection(self):
        # 创建连接
        self.milvus = MilvusClient(
            uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}",
            user=MILVUS_USERNAME,
            password=MILVUS_PASSWORD,
        )
        self.do_create_kb(metric_type=self.metric_type)
    @timeit
    def do_search(
        self,
        query: str = None,
        topk: int = VECTOR_SEARCH_TOP_K,
        score_threshold: float = CHUNK_VECTOR_SEARCH_SCORE_THRESHOLD,
        append_fields: List[str] = None,
        query_vector: List[float] = None,
    ):
        # embeddings = embed_texts_api(query)
        embeddings = query_vector if query_vector else embed_texts_api(query)
        search_params = {
            "metric_type": self.metric_type,  # "L2" IP是Inner Product，越大越接近，L2是欧式距离，越小越接近
            "offset": 0,
            "ignore_growing": False,
            "params": {
                "nprobe": 10,
                # pymilvus 2.2.x版本没有作用，2.3以后才有用
                # search for vectors with a distance greater than score_threshold
                # "radius": score_threshold,
                # # filter out most similar vectors with a distance greater than or equal to 1.0
                # "range_filter" : 1.0
            },
        }

        _filter = None
        output_fields = ["document_uuid", "filename", "chunk_id", "raw_text"]
        if append_fields:
            if isinstance(append_fields, str):
                append_fields = [append_fields]
            output_fields.extend(append_fields)
        result = self.milvus.search(
            self.kb_name,
            embeddings,
            search_params=search_params,
            limit=topk,
            # filter=_filter,
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
        return [doc["entity"] for doc in docs]

    @timeit
    def do_add_doc(self, docs: List[dict]) -> List[str]:
        qs = []
        rest_docs = []
        for i, doc in enumerate(docs):
            raw_text = doc.get("raw_text")
            raw_text_enhanced = doc.get("raw_text_enhanced")
            if raw_text_enhanced:
                q = raw_text_enhanced + "\n\n" + raw_text
            else:
                q = raw_text
            if not q:
                continue
            qs.append(q)
            rest_docs.append(doc)
        qvs = np.array(embed_texts_api(qs))
        for i, doc in enumerate(rest_docs):
            rest_docs[i]["vector"] = qvs[i]
            raw_text = rest_docs[i]["raw_text"]
            if get_num_tokens_from_messages(raw_text) > self.MAX_CHUNK_LEN or len(raw_text) >= self.MAX_CHUNK_LEN:
                # raw_text = raw_text[: self.MAX_CHUNK_LEN - 1]
                rest_docs[i]["raw_text"] = raw_text[:512]
        docs = rest_docs
        pks = self.milvus.insert(self.kb_name, docs, progress_bar=True)
        return pks

    def delete_doc(self, docs: List[dict] = None, field="document_uuid"):
        ids = [doc.get(field) for doc in docs if doc.get(field)]
        return self.do_delete_doc(ids=ids)

    def do_delete_doc(self, ids: List[str] = None) -> List[str]:
        """根据ids删除对应的索引"""
        print(f"document_uuid in {ids}")
        docs = self.milvus.query(
            self.kb_name,
            filter=f"document_uuid in {ids}",
            output_fields=["document_uuid"],
        )
        ids = [doc["id"] for doc in docs]
        if ids:
            return self.milvus.delete(self.kb_name, pks=ids, progress_bar=True)
        return []

    def do_update_doc(self, docs: List[dict]) -> List[str]:
        # 先删除后添加
        self.delete_doc(docs=docs)
        pks = self.do_add_doc(docs)
        return pks


default_chunk_db = MilvusChunkDBService(
    knowledge_base_name=DEFAULT_MILVUS_CHUNK_DB_NAME
)

if __name__ == "__main__":
    # milvus_index_kb = MilvusKBService(knowledge_base_name='test_rb')

    print(default_chunk_db.kb_exists())

    # print(default_chunk_db.do_search("你好"))

    # pks = default_chunk_db.do_add_doc([{"raw_text": "你好"}])
    # print(pks)

    # text = "湖南地区育儿假、独生子女父母护理假执行方案"
    # print(default_chunk_db.do_search(text))

    # default_chunk_db.do_delete_kb()

    # print(default_chunk_db.kb_exists())

    # default_chunk_db.delete_doc([{
    #     "document_uuid": 'ef1c8df8555411efb2403ccd366871d8'
    # }])

    document_uuid = "67a75db05ec511efbdbf0242ac110005"
