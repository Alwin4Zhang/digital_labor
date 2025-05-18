import sys
sys.path.append('./')

import torch
import logging
import numpy as np
from typing import Any, Dict, List, Text, Tuple, Optional,Type

from nlu.components import Component
from nlu.message import Message
from nlu.featurizers.featurizer import DenseFeaturizer
from nlu.tokenizers.lm_tokenizer import LanguageModelTokenizer

from transformers import BertModel,GPT2Model,RobertaModel,AutoModel
device = "cuda:0" if torch.cuda.is_available() else "cpu"

model_class_dict = {
    "bert": BertModel,
    "gpt2": GPT2Model,
    "roberta": RobertaModel,
    "auto": AutoModel
}

# logger = logging.getLogger(__name__)
from configs.apollo_config import logger

class LanguageModelFeaturizer(DenseFeaturizer):
    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        
        self._load_model()
    
    def _load_model(self):
        """Try loading the model"""
        self.model_name = self.component_config.get("model_name","auto")
        if self.model_name not in model_class_dict:
            raise KeyError(
                f"'{self.model_name}' not a valid model name. Choose from "
                f"{str(list(model_class_dict.keys()))}or create"
                f"a new class inheriting from this class to support your model."
            )
        self.model_name_or_path = self.component_config['model_name_or_path']
        self.model = model_class_dict[self.model_name].from_pretrained(self.model_name_or_path)
        logger.debug(f"Loading Tokenizer and Model for {self.model_name}")
    
    @classmethod
    def required_components(cls) -> List[Type["Component"]]:
        return [LanguageModelTokenizer]
    
    def process(self, message: Message, **kwargs: Any) -> None:
        self._set_lm_features(message=message)
    
    def _set_lm_features(self,message:Message) -> Any:
        input_ids = message.get("input_ids")
        attention_mask = message.get("attention_mask")
        text_embeddings = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask).pooler_output
        
        message.set("language_dense_features",text_embeddings)