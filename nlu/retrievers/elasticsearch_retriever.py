import os

from typing import Any, Dict, List, Text, Tuple, Optional, Union
from nlu.retrievers.retriever import Retriever
from nlu.message import Message
from chains.modules.custom_elasticsearch_retriever import MyCustomElasticSearchRetriever

class ElasticsearchRetriever(Retriever):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        
        elasticsearch_url = self.component_config.get('elasticsearch_url',"http://localhost:9200")
        index_name = self.component_config.get("index")
        self.retriever = MyCustomElasticSearchRetriever.create(
            elasticsearch_url=elasticsearch_url,
            index_name=index_name
        )
        
    def process(self, message: Message, **kwargs: Any) -> None:
        text = message.get("text")
        docs = self.retriever._get_relevant_documents(query=text)
        message.set("candidates",docs)