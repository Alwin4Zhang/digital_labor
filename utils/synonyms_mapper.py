import os
import re
import sys
import logging
from typing import Any, Dict, Optional, Text,List

_dir = os.path.dirname(os.path.dirname(__file__))
dictionary_path = os.path.join(_dir,"nlu/data/synonyms.txt")
print(dictionary_path)

from configs.apollo_config import logger

# logger = logging.getLogger(__name__)

class SynonymsMapper(object):
    def __init__(self,synonyms: Optional[Dict[Text,Any]] = None):
        self.synonyms = synonyms if synonyms else {}
        if dictionary_path is not None:
            self.load_custom_dictionary(dictionary_path)
            
    def load_custom_dictionary(self,path: Text) -> None:
        """Load all the custom dictionaries stored in the path.

        More information about the dictionaries file format can
        be found in the documentation of jieba.
        https://github.com/fxsjy/jieba#load-dictionary
        """
        logger.info(f"Loading Synonyms Dictionary at {path}")
        with open(path,'r',encoding='utf-8') as rf:
            for line in rf:
                pairs = re.split(r'[,|， ]',line.strip())
                for w in pairs[1:]:
                    self.synonyms[w] = pairs[0]
                    
    def process(self,entities,keep_dups=False) -> List : 
        new_entities = []
        for entity in entities:
            if entity in self.synonyms:
                entity = self.synonyms[entity]
            if keep_dups:
                new_entities.append(entity)
                continue
            if entity not in new_entities:
                new_entities.append(entity)
        return new_entities
           
synonyms_mappor = SynonymsMapper()           
 
if __name__ == '__main__':
    entities = ['学习期','试用期','考核']
    new_entities = synonyms_mappor.process(entities=entities,keep_dups=False)
    print(new_entities)