import os
import logging
import pickle

from functools import lru_cache
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from typing import Any, Dict, List, Text, Tuple, Optional, Union
from nlu.retrievers.retriever import Retriever
from nlu.message import Message
from vectorstores import MyCustomFAISS
from configs.model_config import CACHED_VS_NUM,EMBEDDING_DEVICE,EMBEDDING_MODEL,embedding_model_dict,VECTOR_SEARCH_TOP_K
from configs.apollo_config import logger

# logger = logging.getLogger(__name__)

# patch HuggingFaceEmbeddings to make it hashable
def _embeddings_hash(self):
    return hash(self.model_name)

HuggingFaceEmbeddings.__hash__ = _embeddings_hash

@lru_cache(CACHED_VS_NUM)
def load_vector_store(vs_path, embeddings):
    return MyCustomFAISS.load_local(vs_path, embeddings)


class FaissRetriever(Retriever):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        
        vs_path = self.component_config.get('vs_path')
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dict[EMBEDDING_MODEL],
                                                model_kwargs={'device': EMBEDDING_DEVICE})
        self.retriever = load_vector_store(vs_path,self.embeddings)
        doc_answer_path = os.path.join(os.path.dirname(vs_path), 'docs_answer', 'docs.pkl')
        self.docs_answer = None
        if os.path.exists(doc_answer_path):
            with open(doc_answer_path, 'rb') as rf:
                self.docs_answer = pickle.load(rf)
            logger.info("Successfully loaded doc answers with pickle...")
        
    def process(self, message: Message, **kwargs: Any) -> None:
        text = message.get("text")
        docs = self.retriever.similarity_search_with_score(text,k=VECTOR_SEARCH_TOP_K)
        related_content_docs = []
        for i in docs:
            idx, q = i[0], i[1]
            content = q + '\n' + self.docs_answer[idx]
            related_content_docs.append(content)
        message.set("candidates",related_content_docs)