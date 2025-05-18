import logging
from typing import Any, Dict, List, Text, Tuple, Optional, Union

from langchain.embeddings.huggingface import HuggingFaceEmbeddings

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from nlu.message import Message
from nlu.rankers.ranker import Ranker

from configs.model_config import EMBEDDING_DEVICE,RERANK_MODEL,RERANK_INSTRUCTION,TITLE_WEIGHT,embedding_model_dict
from configs.apollo_config import logger
# logger = logging.getLogger(__name__)

class QQDRanker(Ranker):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        self.model = SentenceTransformer(embedding_model_dict[RERANK_MODEL])
        self.use_keywords = self.component_config.get("use_keywords",False)
        
    def process(self, message: Message, **kwargs: Any) -> None:
        text = message.get('text')
        keywords = message.get("keywords",[])
        if self.use_keywords and keywords:
            text = ' '.join(keywords)
        candidates = message.get("candidates")
        titles,contents = [],[]
        for cand in candidates:
            lines = cand.splitlines()
            title,content = lines[0],'\n'.join(lines[1:])
            titles.append(title)
            contents.append(content)
        q_embs = self.model.encode([text],normalize_embeddings=True)
        q_enhanced_embs = self.model.encode([RERANK_INSTRUCTION + text],normalize_embeddings=True)
        title_embs = self.model.encode(titles,normalize_embeddings=True)
        content_embs = self.model.encode(contents,normalize_embeddings=True)
        qq_scores = q_embs @ title_embs.T
        qd_scores = q_enhanced_embs @ content_embs.T
        total_scores = TITLE_WEIGHT *  qq_scores + (1 - TITLE_WEIGHT) * qd_scores
        sorted_indices = np.argsort(total_scores[0])[::-1]
        message.set("sorted_candidates",[candidates[idx] for idx in sorted_indices])
        
        