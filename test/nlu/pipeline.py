import os
import sys
sys.path.append('./')

import time
from pprint import pprint

from nlu.interpreter import Interperter

DEFAULT_PIPELINE = [
    "KeywordExtractor"
]

text = "工伤期间工资怎么算？"

interpretor = Interperter(pipeline=DEFAULT_PIPELINE)

start = time.time()
results = interpretor.parse(input=text)
pprint(results)

print(time.time()-start)