import uuid
from typing import Any, Iterable, List, Tuple

from langchain.docstore.document import Document
from langchain.retrievers import ElasticSearchBM25Retriever
from langchain.callbacks.manager import CallbackManagerForRetrieverRun


class MyElasticSearchBM25Retriever(ElasticSearchBM25Retriever):
    """`My custom Elasticsearch` retriever that uses `BM25`."""

    @classmethod
    def create(cls,
               elasticsearch_url: str,
               index_name: str,
               k1: float = 2,
               b: float = 0.75) -> ElasticSearchBM25Retriever:
        """
        Create a ElasticSearchBM25Retriever from a list of texts.

        Args:
            elasticsearch_url: URL of the Elasticsearch instance to connect to.
            index_name: Name of the index to use in Elasticsearch.
            k1: BM25 parameter k1.
            b: BM25 parameter b.

        Returns:

        """
        from elasticsearch import Elasticsearch

        # Create an Elasticsearch client instance
        es = Elasticsearch(elasticsearch_url)
        # Define the index settings and mappings
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
                    "k1": k1,
                    "b": b,
                }
            },
        }

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
        # get all indices startswith langchain
        indices = es.cat.indices(index='langchain*', format='json')
        index_names = [index['index'] for index in indices]
        if index_name in index_names:
            return cls(client=es, index_name=index_name)
        # Create the index with the specified settings and mappings
        es.indices.create(index=index_name,
                          mappings=mappings,
                          settings=settings)
        return cls(client=es, index_name=index_name)

    def add_texts(self,
                  pairs: Iterable[Tuple],
                  refresh_indices: bool = True) -> List[str]:
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
        bulk(self.client, requests)

        if refresh_indices:
            self.client.indices.refresh(index=self.index_name)
        return ids

    def _get_relevant_documents(
            self, query: str, *,
            run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        query_dict = {
            "query": {
                "bool": {
                    "should": [{
                        "match": {
                            "title": query
                        }
                    }, {
                        "match": {
                            "content": query
                        }
                    }]
                }
            }
        }
        res = self.client.search(index=self.index_name, body=query_dict)

        docs = []
        for r in res["hits"]["hits"]:
            docs.append(Document(page_content=r["_source"]["content"]))
        return docs


if __name__ == '__main__':
    elasticsearch_url = "http://localhost:9200"
    # retriever = MyElasticSearchBM25Retriever.create(elasticsearch_url,"langchain-index-5")

    # retriever.add_texts([
    #     ("今天天气不错","天气预报今天晴"),
    #     ("今天我想出门","今天我要出门采买年货"),
    #     ("南京市长是谁?","南京市长江大桥参观长江大桥建设"),
    #     ("市里突击检查","市区建设突击检查完善工作")
    # ])

    # docs = retriever.get_relevant_documents("今天")
    # print(docs)