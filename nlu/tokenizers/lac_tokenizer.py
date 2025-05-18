import glob
import logging
import os
import shutil
import typing
from LAC import LAC
from typing import Any, Dict, List, Optional, Text

from nlu.components import Component
from nlu.message import Message
from nlu.tokenizers.tokenizer import Token,Tokenizer
from configs.apollo_config import logger

# logger = logging.getLogger(__name__)


class LACTokenizer(Tokenizer):
    """百度LAC分词器"""
    language_list = ["zh"]
    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None,mode='lac') -> None:
        super().__init__(component_config)
        
        self.lac = LAC(mode=mode)
        self.dictionary_path = self.component_config.get("dictionary_path")
        
        if self.dictionary_path is not None:
            self.load_custom_dictionary(self.dictionary_path)
            
    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["lac"]

    def load_custom_dictionary(self,path: Text) -> None:
        lac_userdicts = glob.glob(f"{path}/*")
        for lac_userdict in lac_userdicts:
            logger.info(f"Loading LAC User Dictionary at {lac_userdict}")
            self.lac.load_customization(lac_userdict,sep=None)
            
    def tokenize(self, message: Message) -> List[Token]:
        text = message.get("text")
        tokens = []
        lac_results = self.lac.run(text)
        idx = 0
        for word,flag in lac_results:
            tokens.append(Token(word,start=idx,pos=flag))
            idx += len(word)
        return tokens