import sys
import os

sys.path.append('./')

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from fuzzywuzzy import fuzz

from db.service.elasticsearch_kb_service import ElasticsearchKBService, default_es_db
from db.session import with_session
from db.models.knowledge_base_model import KnowledgeBaseModel, DocumentBaseModel
from configs.apollo_config import ELASTICSEARCH_URL, INDEX_NAME, ES_USERNAME, ES_PASSWORD
from configs.constants import DEFAULT_MAPPINGS, DEFAULT_SETTINGS

from chains.local_rag import LocalRAG


class MyCustomElasticsearchKBService(ElasticsearchKBService):

    def __init__(self, knowledge_base_name, embed_model: str = ...):
        super().__init__(knowledge_base_name, embed_model)
        self._init_db_connection()

    def _init_db_connection(self):
        # 创建连接
        if ES_USERNAME and ES_PASSWORD:
            self.client = Elasticsearch(ELASTICSEARCH_URL,
                                        http_auth=(ES_USERNAME, ES_PASSWORD),
                                        timeout=30,
                                        max_retries=10,
                                        retry_on_timeout=True)
        else:
            self.client = Elasticsearch(ELASTICSEARCH_URL,
                                        timeout=30,
                                        max_retries=10,
                                        retry_on_timeout=True)

    def do_create_kb(self):
        """创建索引"""
        if not self.kb_exists():
            # Create the index with the specified settings and mappings
            self.client.indices.create(index=self.kb_name,
                                       body={
                                           "settings": DEFAULT_SETTINGS,
                                           "mappings": DEFAULT_MAPPINGS
                                       })
            print(
                f"create elasticsearch collection: {self.kb_name} success!", )


@with_session
def list_qas_from_db(session, release_status):
    qas = session.query(KnowledgeBaseModel).filter_by(
        release_status=release_status).all()
    qas = [qa.to_dict() for qa in qas]
    return qas


if __name__ == "__main__":
    # qas = list_qas_from_db(release_status='released')
    # print(qas)

    # custom_elasticsearch_kb_service = MyCustomElasticsearchKBService(
    #     knowledge_base_name=INDEX_NAME)
    # custom_elasticsearch_kb_service.create_kb()

    docs = [
        {
            "id": 1,
            "question": "你是谁",
            "answer": "我是小天"
        },
        {
            "id": 2,
            "question": "今天星期几",
            "answer": "今天星期三"
        },
        {
            "id": 3,
            "question": "今天周几",
            "answer": "今天星期三"
        },
        {
            "id": 4,
            "question": "今天是哪一天",
            "answer": "今天星期四"
        },
        {
            "id": 5,
            "question": "今天是那一天呀",
            "answer": "今天星期四"
        },
    ]

    # hits = custom_elasticsearch_kb_service.do_search(query="你好")
    # print(custom_elasticsearch_kb_service.update_doc(docs))
    # hits = custom_elasticsearch_kb_service.do_search(query="你好")
    # print(hits)

    # print(default_es_db.delete_doc(docs=docs))

    # res = custom_elasticsearch_kb_service.question_validate(question="你是谁")
    # print(res)

    local_rag = LocalRAG()
    local_rag.question_validate(question="什么是人工智能")