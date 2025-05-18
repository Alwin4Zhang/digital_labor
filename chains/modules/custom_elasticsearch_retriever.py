import uuid
from typing import Any, Iterable, List, Tuple
from langchain.docstore.document import Document
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class MyCustomElasticSearchRetriever(object):
    """`My custom Elasticsearch` retriever that uses `BM25`."""

    def __init__(self, client: Any, index_name: str) -> None:
        self.client = client
        self.index_name = index_name

    @classmethod
    def create(cls,
               elasticsearch_url: str,
               index_name: str,
               settings=None,
               mappings=None) -> Any:
        """
        Create a ElasticSearchBM25Retriever from a list of texts.

        Args:
            elasticsearch_url: URL of the Elasticsearch instance to connect to.
            index_name: Name of the index to use in Elasticsearch.
            settings: custom index settings.
            mappings: custom index mappings.

        Returns:
        """
        es = Elasticsearch(elasticsearch_url)
        if not settings:
            settings = {
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "standard"
                        }
                    }
                },
                "similarity": {
                    "custom_bm25": {
                        "type": "BM25",
                        "k1": 2,
                        "b": 0.75,
                    }
                },
            }
        if not mappings:
            mappings = {
                "properties": {
                    "title": {
                        "type": "text",
                        "similarity": "custom_bm25",
                    },
                    "content": {
                        "type": "text",
                        "similarity":
                        "custom_bm25",  # Use the custom BM25 similarity
                    }
                }
            }

        indices = es.cat.indices(index='langchain*', format='json')
        index_names = [index['index'] for index in indices]
        if index_name in index_names:
            return cls(client=es, index_name=index_name)

        es.indices.create(index=index_name,
                          mappings=mappings,
                          settings=settings)
        return cls(es, index_name)

    def add_texts(self,
                  pairs: Iterable[Tuple],
                  refresh_indices: bool = True,
                  use_vectors: bool = False) -> List[str]:
        """Run more texts through the embeddings and add to the retriever.

        Args:
            texts: Iterable of strings to add to the retriever.
            refresh_indices: bool to refresh ElasticSearch indices

        Returns:
            List of ids from adding the texts into the retriever.
        """
        try:
            from elasticsearch.helpers import bulk
        except ImportError:
            raise ValueError(
                "Could not import elasticsearch python package. "
                "Please install it with `pip install elasticsearch`.")

        requests = []
        ids = []
        if not use_vectors:
            for i, (title, content) in enumerate(pairs):
                _id = str(uuid.uuid4())
                request = {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "title": title,
                    "content": content,
                    "_id": _id,
                }
                ids.append(_id)
                requests.append(request)
        else:
            for i, (title, content, vector) in enumerate(pairs):
                _id = str(uuid.uuid4())
                request = {
                    "_index": self.index_name,
                    "_id": _id,
                    "_source": {
                        "title": title,
                        "content": content,
                        "content_vector": vector
                    }
                }
                ids.append(_id)
                requests.append(request)
        bz = 50
        total_range = len(requests) // bz if len(requests) % bz == 0 else (
            len(requests) // bz + 1)
        for i in range(total_range):
            tpr = requests[i * bz:(i + 1) * bz]
            bulk(self.client, tpr, raise_on_error=False)

        if refresh_indices:
            self.client.indices.refresh(index=self.index_name)
        return ids

    def _get_relevant_documents(self,
                                query: str = None,
                                query_kws: List = None,
                                dsl=None,
                                topk=5) -> List[Document]:
        if not dsl:
            dsl = {
                "_source": {
                    "excludes": ["title_vector"]
                },
                "from": 0,
                "size": topk,
                "query": {
                    "bool": {
                        "should": [{
                            "match": {
                                "title": {
                                    "query": query,
                                    "analyzer": "ikSearchAnalyzer",
                                    "boost": 1.1
                                }
                            }
                        }, {
                            "match": {
                                "content": {
                                    "query": query,
                                    "analyzer": "ikSearchAnalyzer",
                                    "boost": 0.5
                                }
                            }
                        }, {
                            "terms": {
                                "title_keywords": query_kws,
                                "boost": 1.5
                            }
                        }, {
                            "terms": {
                                "content_keywords": query_kws,
                                "boost": 0.5
                            }
                        }]
                    }
                }
            }
        res = self.client.search(index=self.index_name, body=dsl)

        # docs = []
        # for r in res["hits"]["hits"]:
        #     docs.append(Document(page_content=r["_source"]["content"]))
        # return docs
        return res["hits"]["hits"]


if __name__ == '__main__':
    # elasticsearch_url = "http://localhost:9200"
    elasticsearch_url = "http://10.60.236.77:9200"
    # retriever = MyCustomElasticSearchRetriever.create(elasticsearch_url,"langchain-index-8")

    # retriever.add_texts([
    #     ("今天天气不错","天气预报今天晴"),
    #     ("今天我想出门","今天我要出门采买年货"),
    #     ("南京市长是谁?","南京市长江大桥参观长江大桥建设"),
    #     ("市里突击检查","市区建设突击检查完善工作")
    # ])

    # docs = retriever._get_relevant_documents("产假")
    # print(docs)