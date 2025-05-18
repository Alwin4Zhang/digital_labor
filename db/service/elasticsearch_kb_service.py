import sys

sys.path.append("./")
# import logging
from typing import List, Dict, Optional

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from fuzzywuzzy import fuzz

from langchain.schema import Document

from configs.apollo_config import ELASTICSEARCH_URL, ES_USERNAME, ES_PASSWORD
from configs.apollo_config import DEFAULT_ELASTICSEARCH_KB_NAME
from configs.apollo_config import logger
from configs.constants import DEFAULT_MAPPINGS, DEFAULT_SETTINGS

from db.service.base import KBService, SupportedVSType
from db.embedding_utils import embed_texts_api, embed_documents_api




class ElasticsearchKBService(KBService):
    dim: int = 1024

    def __init__(self, knowledge_base_name, embed_model: str = ...):
        super().__init__(knowledge_base_name, embed_model)
        self._init_db_connection()

    def _init_db_connection(self):
        # 创建连接
        if ES_USERNAME and ES_PASSWORD:
            self.client = Elasticsearch(
                ELASTICSEARCH_URL,
                http_auth=(ES_USERNAME, ES_PASSWORD),
                timeout=30,
                max_retries=10,
                retry_on_timeout=True,
            )
        else:
            self.client = Elasticsearch(
                ELASTICSEARCH_URL, timeout=30, max_retries=10, retry_on_timeout=True
            )
        self.do_create_kb()

    @property
    def vs_type(self) -> str:
        return SupportedVSType.ES

    def kb_exists(self):
        return self.kb_name in [
            index["index"]
            for index in self.client.cat.indices(index="*", format="json")
        ]

    def do_create_kb(self):
        """创建索引"""
        if not self.kb_exists():
            # Create the index with the specified settings and mappings
            # self.client.indices.create(index=self.kb_name,
            #                            mappings=DEFAULT_MAPPINGS,
            #                            settings=DEFAULT_SETTINGS)
            self.client.indices.create(
                index=self.kb_name,
                body={"settings": DEFAULT_SETTINGS, "mappings": DEFAULT_MAPPINGS},
            )
            print(
                f"create elasticsearch collection: {self.kb_name} success!",
            )

    def do_delete_kb(self):
        """删除索引"""
        self.client.indices.delete(index=self.kb_name)

    def do_search(
        self,
        query: str,
        topk: int = 10,
        score_threshold: float = None,
        dsl: bool = None,
    ):
        if not dsl:
            dsl = {
                "_source": {"excludes": ["question_vector"]},
                "from": 0,
                "size": topk,
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "question": {
                                        "query": query,
                                        "analyzer": "ikSearchAnalyzer",
                                        "boost": 1.1,
                                    }
                                }
                            },
                            {
                                "match": {
                                    "answer": {
                                        "query": query,
                                        "analyzer": "ikSearchAnalyzer",
                                        "boost": 0.5,
                                    }
                                }
                            },
                        ]
                    }
                },
            }
        res = self.client.search(index=self.kb_name, body=dsl)
        hits = res["hits"]["hits"]
        if score_threshold:
            hits = [hit for hit in hits if hit["_score"] >= score_threshold]
        return hits

    def suggest(self, query):
        """搜索提示"""
        dsl = {
            "_source": {"excludes": ["question_vector"]},
            "query": {
                "script_score": {
                    "query": {"match_phrase_prefix": {"question": {"query": query}}},
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'question_vector') + 1.0",
                        "params": {"queryVector": embed_texts_api(query)[0]},
                    },
                }
            },
        }
        res = self.client.search(index=self.kb_name, body=dsl)
        return res["hits"]["hits"]

    def add_doc(self, docs: List[dict] = None, use_vectors: bool = True):
        return self.do_add_doc(docs, use_vectors=use_vectors)

    def do_add_doc(self, docs: List[dict], use_vectors: bool = True) -> List[Dict]:
        actions, ids = [], []
        for doc in docs:
            _id = doc.get("id")
            question = doc.get("question")
            answer = doc.get("answer")
            document_uuid = doc.get("document_uuid","")
            filename = doc.get("filename","")
            if not _id or not question.strip() or not answer.strip():
                continue
            action = {
                "_op_type": "create",
                "_index": self.kb_name,
                "question": question,
                "answer": answer,
                "document_uuid": document_uuid,
                "filename": filename,
                "_retry_on_conflict": 3,
                "_id": _id,
            }
            if use_vectors:
                action.update(
                    {
                        "_source": {
                            "question": question,
                            "answer": answer,
                            "document_uuid": document_uuid,
                            "filename": filename,
                            "question_vector": embed_texts_api(question)[0],
                        }
                    }
                )
            ids.append(_id)
            actions.append(action)
        self.do_batch_actions(actions=actions)
        self.client.indices.refresh(index=self.kb_name)
        return ids

    def do_batch_actions(self, actions, bz=50):
        """分批执行action"""
        success = 0
        total_range = (
            len(actions) // bz if len(actions) % bz == 0 else (len(actions) // bz + 1)
        )
        for i in range(total_range):
            tpr = actions[i * bz : (i + 1) * bz]
            s,f = bulk(self.client, tpr, raise_on_error=False)
            success += s
        return success
    
    def delete_doc(self, docs: List[dict] = None,field: str = "id"):
        ids = [doc[field] for doc in docs]
        return self.do_delete_doc(ids)

    def do_delete_doc(self, ids: List[str] = None):
        actions = []
        for _id in ids:
            actions.append({"_op_type": "delete", "_index": self.kb_name, "_id": _id})
        self.do_batch_actions(actions=actions)
        success = self.client.indices.refresh(index=self.kb_name)
        return ids if success == len(actions) else []

    def do_update_doc(self, docs: List[dict] = None, use_vectors: bool = True):
        actions, ids = [], []
        for doc in docs:
            _id = doc.get("id")
            question = doc.get("question")
            answer = doc.get("answer")
            document_uuid = doc.get("document_uuid","")
            filename = doc.get("filename","")
            if not _id or not question.strip() or not answer.strip():
                continue
            action = {
                "_op_type": "index",  # index create and update;btw update only update,create only create
                "_index": self.kb_name,
                "_id": _id,
                "_retry_on_conflict": 3,
            }
            if use_vectors:
                action.update(
                    {
                        "question": question,
                        "answer": answer,
                        "document_uuid": document_uuid,
                        "filename": filename,
                        "question_vector": embed_texts_api(question)[0],
                    }
                )
            ids.append(_id)
            actions.append(action)
        self.do_batch_actions(actions=actions)
        self.client.indices.refresh(index=self.kb_name)
        return ids


default_es_db = ElasticsearchKBService(
    knowledge_base_name=DEFAULT_ELASTICSEARCH_KB_NAME
)

if __name__ == "__main__":
    docs = [
        {"id": 1, "question": "你是谁", "answer": "我是小天"},
        {"id": 2, "question": "今天星期几", "answer": "今天星期三","filename": "a.docx"},
        {"id": 3, "question": "今天周几", "answer": "今天星期三"},
        {"id": 4, "question": "今天是哪一天", "answer": "今天星期四","filename": "b.docx"},
        {"id": 5, "question": "今天是那一天呀", "answer": "今天星期四"},
    ]

    # 创建索引
    # default_es_db.kb_exists()
    # default_es_db.do_create_kb()

    # 添加索引
    # print(default_es_db.add_doc(docs=docs))

    # # print(default_es_db.delete_doc(docs=docs))

    # 删除索引
    # # default_es_db.delete_kb()

    # 搜索
    # res = default_es_db.do_search(query="你是哪位?")
    # print(res)

    # 更改索引
    # docs = [{"id": 1, "question": "你是哪位", "answer": "我是智能助手小天"}]

    print(default_es_db.update_doc(docs))

    # print(default_es_db.delete_doc(docs=docs))

    # print(default_es_db.suggest(query="今天"))

    # default_es_db.question_validate(question="你是谁")
