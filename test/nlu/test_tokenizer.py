import sys

sys.path.append('./')

from nlu.tokenizers.jieba_tokenizer import JiebaTokenizer
from nlu.message import Message

text = "今天天气不错,我想出去一趟"
message = Message(text=text, time="2023-11-17")
message.set("text", text)
jieba_tokenizer = JiebaTokenizer()

tokens = jieba_tokenizer.tokenize(message)
for tk in tokens:
    print(tk.text, tk.pos)
