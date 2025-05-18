import sys

sys.path.append('./')

from nlu.extractors.keyword_extractor import KeywordExtractor
from nlu.message import Message

text = "工伤期间工资怎么算？"
message = Message(text=text, time="2023-11-17")
message.set("text", text)

component_config = {"kw_backend": "custom"}

extractor = KeywordExtractor(component_config=component_config)

extractor.process(message=message)
print(message.as_dict())