import os
import glob
import logging
from typing import Any, Dict, List,Optional, Text
import jieba
import jieba.posseg as pseg
from jieba.analyse import tfidf,textrank
from LAC import LAC
import numpy as np

from nlu.extractors.extractor import EntityExtractor
from nlu.message import Message

# logger = logging.getLogger(__name__)
from configs.apollo_config import logger

FILTER_POS = ['n','nr','ns','nt','nw','nz','v','vn','vd','f','s','t','PER','LOC','ORG','TIME','x']

class KeywordExtractor(EntityExtractor):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        
        self.dictionary_path = self.component_config.get("dictionary_path")
        if self.dictionary_path is not None:
            self.load_custom_dictionary(self.dictionary_path)
            
        self.backend = self.component_config.get("kw_backend","custom")
        if self.backend == 'lac':
            lac = LAC(mode='rank')
            self.extractor = lac.run
        elif self.backend == 'tfidf':
            self.extractor = tfidf
        elif self.backend == 'textrank':
            self.extractor = textrank
        elif self.backend == 'custom':
            self.extractor = jieba.analyse.extract_tags
            
    @classmethod
    def required_components(cls) -> List[Text]:
        return ["jieba","LAC"]
    
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
    
    def process(self, message: Message,topk = 5,**kwargs: Any) -> None:
        text = message.get("text")
        if self.backend == 'custom':
            kws = self.extractor(text,topK=topk,withWeight=True, allowPOS=FILTER_POS)
            kws = [k[0] for k in kws]
        else:
            kws = self.extractor(text)
        if self.backend != 'lac':
            message.set("keywords",kws[:topk])
        else:
            weight_sorted_indices = np.argsort(kws[-1])[::-1]
            kws = [kws[0][idx] for idx in weight_sorted_indices[:topk]]
            message.set("keywords",kws)
        
            
