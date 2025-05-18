import glob
import logging
import os
import shutil
import typing
from typing import Any, Dict, List, Optional, Text
import jieba
import jieba.posseg as pseg
from nlu.components import Component
from nlu.message import Message
from nlu.tokenizers.tokenizer import Token,Tokenizer

from configs.apollo_config import logger
# logger = logging.getLogger(__name__)


class JiebaTokenizer(Tokenizer):
    """结巴分词器"""
    language_list = ["zh"]
    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        
        self.dictionary_path = self.component_config.get("dictionary_path")
        
        if self.dictionary_path is not None:
            self.load_custom_dictionary(self.dictionary_path)
            
    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["jieba"]

    @staticmethod
    def load_custom_dictionary(path: Text) -> None:
        """Load all the custom dictionaries stored in the path.

        More information about the dictionaries file format can
        be found in the documentation of jieba.
        https://github.com/fxsjy/jieba#load-dictionary
        """
        jieba_userdicts = glob.glob(f"{path}/*")
        for jieba_userdict in jieba_userdicts:
            logger.info(f"Loading Jieba User Dictionary at {jieba_userdict}")
            jieba.load_userdict(jieba_userdict)
            
    def tokenize(self, message: Message) -> List[Token]:        
        text = message.get("text")
        tokenized = pseg.lcut(text)
        idx = 0
        tokens = []
        for seg in tokenized:
            word,flag = seg.word,seg.flag
            tokens.append(Token(word,start=idx,pos=flag))
            idx += len(word)
        return tokens