# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2023/11/16 21:28:36
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''
import logging
from typing import Text, List, Optional, Dict, Any

from nlu.components import Component
from nlu.message import Message
from configs.apollo_config import logger

# logger = logging.getLogger(__name__)


class Token(object):
    def __init__(self,
                 text:Text,
                 start:int,
                 end:Optional[int]=None,
                 pos:Optional[Text]=None,
                 data:Optional[Dict[Text,Any]] = None,
                 lemma: Optional[Text] = None) -> None:
        self.text = text
        self.start = start
        self.end = end if end else start + len(text)
        self.pos = pos
        
        self.data = data if data else {}
        self.lemma = lemma or text
        
    def set(self,prop:Text,info:Any) -> None:
        self.data[prop] = info
    
    def get(self, prop: Text, default: Optional[Any] = None) -> Any:
        return self.data.get(prop, default)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other,Token):
            return NotImplemented
        return (self.start,self.end,self.text,self.pos,self.lemma) == (
            other.start,
            other.end,
            other.text,
            other.pos,
            other.lemma,
        )
        
    def __lt__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (self.start, self.end, self.text,self.pos, self.lemma) < (
            other.start,
            other.end,
            other.text,
            self.pos,
            other.lemma,
        )

       
class Tokenizer(Component):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""
        super().__init__(component_config)
        
    def tokenize(self,message:Message) -> List[Token]:
        """Tokenizes the text of the provided attribute of the incoming message."""
        raise NotImplementedError
    
    def process(self,message:Message,**kwargs:Any) -> None:
        """Tokenize the incoming message."""
        tokens = self.tokenize(message)
        message.set("tokens",tokens)