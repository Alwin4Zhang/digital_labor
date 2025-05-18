import os
import logging
import re
from typing import Any, Dict, Optional, Text

from nlu.classifiers.classifier import IntentClassifier
from nlu.message import Message

from configs.apollo_config import logger


class KeywordIntentClassifier(IntentClassifier):
    """Intent classifier using simple keyword matching.


    The classifier takes a list of keywords and associated intents as an input.
    A input sentence is checked for the keywords and the intent is returned.

    """
    
    def __init__(self, 
                 component_config: Optional[Dict[Text, Any]] = None,
                 intent_keyword_map: Optional[Dict] = None
                 ):
        super(KeywordIntentClassifier,self).__init__(component_config)
        
        self.intent_key_map = intent_keyword_map or {}
        
    
    def process(self, message: Message, **kwargs: Any) -> None:
        intent_name = self._map_keyword_to_intent(message.text)
        confidence = 0.0 if intent_name is None else 1.0
        intent = {
            "name": intent_name,
            "confidence": confidence
        }
        if message.get("intent") is None or intent is not None:
            message.set("intent",intent)
    
    def _map_keyword_to_intent(self,text:Text) -> Optional[Text]:
        re_flag = 0
        for keyword,intent in self.intent_key_map.items():
            if re.search(r"\b" + keyword + r"\b", text, flags=re_flag):
                logger.debug(
                    f"KeywordClassifier matched keyword '{keyword}' to"
                    f" intent '{intent}'."
                )
                return intent
        logger.debug("KeywordClassifier did not find any keywords in the message.")
        return None