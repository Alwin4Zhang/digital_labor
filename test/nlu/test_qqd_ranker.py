import sys
sys.path.append('./')

from nlu.rankers.qqd_ranker import QQDRanker

from nlu.message import Message

from jieba.analyse import tfidf,textrank

text = "工伤期间工资怎么算？"
keywords = tfidf(text)
message = Message(
    text = text,
    time = "2023-11-17"
)

queries = [
    "我因工受伤了,工伤期间工资怎么发?",
    "我上班的时候受伤了,工资怎么发?",
    "病假工资怎么发？",
    "产假期间工资怎么发",
    "我休婚假扣钱吗？",
    "我休丧假扣钱吗？",
    "我休看护假扣钱吗？",
    "我休节育假扣钱吗？",
    "我请病假了,病假工资怎么扣?",
    "R3系统是什么"
]

candidates = []

for q in queries:
    q = ' '.join(tfidf(q)) + "\n" + ' '.join(tfidf(q))
    candidates.append(q)

message.set("text",text)
message.set("keywords",keywords)
message.set("candidates",candidates)

component_config = {
    "use_keywords": True
}

ranker = QQDRanker(component_config=component_config)

ranker.process(message=message)
print(message.as_dict())