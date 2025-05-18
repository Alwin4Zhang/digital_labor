# -*- coding: utf-8 -*-
"""
  @CreateTime	:  2024/02/19 17:23:31
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
"""
import os
import sys
from typing import List

sys.path.append("./")

from db.service.milvus_kb_service import MilvusKBService
from db.service.elasticsearch_kb_service import ElasticsearchKBService
from utils.llm_util import post_api_for_llm, apost_api_for_llm
from configs.model_config import *
from loader.unstructured_loaders.constants import heading_levels, NORMAL
from db.embedding_utils import embed_documents_api, embed_texts_api

from chains.local_rag import LocalRAG

test_vector_db = MilvusKBService(knowledge_base_name="digital_supermarket")
test_es_db = ElasticsearchKBService(knowledge_base_name="test_supermarket")


class LocalChunkRAG(LocalRAG):

    def __init__(self) -> None:
        super().__init__()

    def recall_most_similar_chunk(self, query):
        recalls = test_vector_db.do_search(query=query, append_fields=["metadata"])
        return recalls[0] if recalls else []

    def recall_content_under_current_header(self, recall):
        headers = {}
        for k, v in recall["metadata"].items():
            if k in heading_levels and heading_levels[k] < 10:
                headers[k] = v

        dsl = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "metadata.file_name.keyword": recall["metadata"][
                                    "file_name"
                                ]
                            }
                        }
                    ]
                }
            }
        }

        if headers:
            for header, v in headers.items():
                dsl["query"]["bool"]["must"].append(
                    {"match": {f"metadata.{header}.data.keyword": v["data"]}}
                )

        res = test_es_db.client.search(index=test_es_db.kb_name, body=dsl)

        total_content = ""
        for hit in sorted(
            res["hits"]["hits"], key=lambda x: x["_source"]["chunk_index"]
        ):
            _source = hit["_source"]
            metadata = _source.get("metadata")
            chunk_raw_text = metadata.get("html")
            total_content += chunk_raw_text

        return total_content.replace("\n", "")

    def recall_most_similar_chunk_complex(self, query, topk=5, thres=1.0):
        """使用es的向量和关键词同时检索"""
        dsl = {
            "_source": {"excludes": ["question_vector"]},
            "query": {
                "script_score": {
                    "query": {
                        "match": {
                            "question": {"query": query, "analyzer": "ikSearchAnalyzer"}
                        }
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'question_vector') + 1.0",
                        "params": {"queryVector": embed_texts_api(query)[0]},
                    },
                }
            },
        }
        res = test_es_db.client.search(index=test_es_db.kb_name, body=dsl)
        hits = res["hits"]["hits"]
        # return hits[0]['_source'] if hits else {}
        # todo:修改为返回多条文件
        return [hit["_source"] for hit in hits if hit["_score"] >= thres][:topk]

    def do_search(self, query):
        # rec = self.recall_most_similar_chunk_complex(query=query)
        # if not rec:
        #     return None, None
        # file_name = rec['metadata']['file_name']
        # return self.recall_content_under_current_header(recall=rec), file_name

        recs = self.recall_most_similar_chunk_complex(query=query)
        if not recs:
            return None, None
        return [self.recall_content_under_current_header(recall=rec) for rec in recs], [
            rec["metadata"]["file_name"] for rec in recs
        ]

    def dialog_onetune(self, query, chat_history=None, is_append: bool = False):
        if not chat_history:
            chat_history = []
        chat_history = self.history_format(chat_history)
        # content, file_name = self.do_search(query=query)
        contents, file_names = self.do_search(query=query)
        if not contents:
            return self.streaming_llm_output(
                query=query,
                chat_history=chat_history[:],
                related_docs=[],
                is_append=is_append,
            )
        else:
            related_docs = [
                {
                    "url": "",
                    "is_source": 1 if i == 0 else 0,
                    "title": file_name,
                    "knowledge_id": None,
                }
                for i, file_name in enumerate(file_names)
            ]
            content = "<h1>下面是匹配到的相关文档内容：</h1>\n"
            for i, (file_name, cont) in enumerate(zip(file_names, contents)):
                content += f"<h2>{i + 1}：文件名称:{file_name}\n</h2>"
                content += "<b>匹配到的内容是：</b>\n"
                content += f"<p>{cont}</p>" + "\n\n"
                content += "-" * 100
            return self.streaming_simu_output(
                query=query,
                content=content,
                related_docs=related_docs[:],
                interval=0.01,
                is_append=is_append,
            )
