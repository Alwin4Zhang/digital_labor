import logging
import os
import typing
import warnings
from typing import Any, Dict, List, Optional, Text, Tuple, Type
import numpy as np

from nlu.classifiers.classifier import IntentClassifier
from nlu.message import Message

from configs.apollo_config import logger

if typing.TYPE_CHECKING:
    import sklearn
    
    
class SklearnIntentClassifier(IntentClassifier):
    
    @classmethod
    def required_components(cls) -> List[Text]:
        return ["sklearn"]