import logging
from typing import Any, Dict, List, Text, Tuple, Optional

from nlu.tokenizers.tokenizer import Token,Tokenizer
from nlu.message import Message

from transformers import BertTokenizer,GPT2Tokenizer,RobertaTokenizer,AutoTokenizer
from transformers import BertModel,GPT2Model,RobertaModel,AutoModel

from configs.apollo_config import logger

model_class_dict = {
    "bert": BertModel,
    "gpt2": GPT2Model,
    "roberta": RobertaModel,
    "auto": AutoModel
}

model_tokenizer_dict = {
    "bert": BertTokenizer,
    "gpt2": GPT2Tokenizer,
    "roberta": RobertaTokenizer,
    "auto": AutoTokenizer
}

# logger = logging.getLogger(__name__)

class LanguageModelTokenizer(Tokenizer):
    """Tokenizer using transformer based language models."""
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
        self.tokenizer = model_tokenizer_dict[self.model_name].from_pretrained(self.model_name_or_path)
        # self.model = model_class_dict[self.model_name].from_pretrained(self.model_name_or_path)
        logger.debug(f"Loading Tokenizer and Model for {self.model_name}")
        
        # self.pad_token_id = self.tokenizer.unk_token_id
        
    @classmethod
    def required_components(cls) -> List[Text]:
        return ["transformers"]
    
    def tokenize(self,text:Text) -> Dict[Text, Any]:
        tokenized_dict = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_offsets_mapping=True,
            return_tensors='pt')
        return tokenized_dict
        
    def process(self,message:Message,**kwargs):
        tokenized_dict = self.tokenize(message.text)
        for k,v in tokenized_dict.items():
            message.set(prop=k,info=v)