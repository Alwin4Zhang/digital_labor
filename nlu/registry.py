import logging
import typing
from typing import Any, Dict, List, Optional, Text, Type

from nlu.components import Component

from nlu.classifiers.keyword_intent_classifier import KeywordIntentClassifier
from nlu.classifiers.sklearn_intent_classifier import SklearnIntentClassifier

from nlu.extractors.entity_synonyms import EntitySynonymsMapper
from nlu.extractors.keyword_extractor import KeywordExtractor

from nlu.featurizers.lm_featurizer import LanguageModelFeaturizer

from nlu.rankers.qqd_ranker import QQDRanker
from nlu.retrievers.elasticsearch_retriever  import ElasticsearchRetriever
from nlu.retrievers.faiss_retriever import FaissRetriever

from nlu.tokenizers.jieba_tokenizer import JiebaTokenizer
from nlu.tokenizers.lac_tokenizer import LACTokenizer
from nlu.tokenizers.lm_tokenizer import LanguageModelTokenizer

# logger = logging.getLogger(__name__)
from configs.apollo_config import logger


component_classes = [
    # classifier
    KeywordIntentClassifier,
    SklearnIntentClassifier,
    # extractor
    EntitySynonymsMapper,
    KeywordExtractor,
    
    # featurziers
    LanguageModelFeaturizer,
    
    # rank
    QQDRanker,
    
    # retriever
    ElasticsearchRetriever,
    FaissRetriever,
    
    # tokenizers
    JiebaTokenizer,
    LACTokenizer,
    LanguageModelTokenizer
]

registered_components = {c.name:c for c in component_classes}

def get_component_class(component_name:Text) -> Type["Component"]:
    if component_name not in registered_components:
        raise f"Failed to find class '{component_name}'\n"
    return registered_components[component_name]