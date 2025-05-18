import os
import glob
import logging
from typing import Any, Dict, List,Optional, Text
import jieba
import jieba.posseg as pseg
from jieba.analyse import tfidf,textrank
from LAC import LAC
import numpy as np

_dir = os.path.dirname(os.path.dirname(__file__))
dictionary_path = os.path.join(_dir,"nlu/data/custom_dic.txt")
print(dictionary_path)
from configs.apollo_config import logger
# logger = logging.getLogger(__name__)

FILTER_POS = ['b','n','nr','ns','nt','nw','nz','v','vn','vd','f','s','t','PER','LOC','ORG','TIME','x']

class KeywordExtractor(object):
    def __init__(self, backend='custom') -> None:        
        self.backend = backend
        if dictionary_path is not None:
            self.load_custom_dictionary(dictionary_path)
        if self.backend == 'lac':
            lac = LAC(mode='rank')
            self.extractor = lac.run
        elif self.backend == 'tfidf':
            self.extractor = tfidf
        elif self.backend == 'textrank':
            self.extractor = textrank
        elif self.backend == 'custom':
            self.extractor = jieba.analyse.extract_tags
    
    def load_custom_dictionary(self,path: Text) -> None:
        """Load all the custom dictionaries stored in the path.

        More information about the dictionaries file format can
        be found in the documentation of jieba.
        https://github.com/fxsjy/jieba#load-dictionary
        """
        logger.info(f"Loading Jieba User Dictionary at {path}")
        jieba.load_userdict(path)
    
    def process(self, text,topk = 5) -> List:
        if self.backend == 'custom':
            kws = self.extractor(text,topK=topk,withWeight=True, allowPOS=FILTER_POS)
            kws = [k[0] for k in kws]
        else:
            kws = self.extractor(text)
        if self.backend != 'lac':
            return kws[:topk]
        else:
            weight_sorted_indices = np.argsort(kws[-1])[::-1]
            kws = [kws[0][idx] for idx in weight_sorted_indices[:topk]]
            return kws
        
keyword_extracter = KeywordExtractor()

if __name__ == '__main__':
    test_text = "北京-考勤-北京产假有多少天？"
    test_text = "我工作满3年,年假有几天？"
    keywords = keyword_extracter.process(test_text)
    print(keywords)