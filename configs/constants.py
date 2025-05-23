special_question_dict = {
    "你身份是什么？": 1,
    "什么是天虹数科？": 1,
    "你知道天虹数科吗?": 1,
    "天虹数科是什么？": 1,
    "介绍一下天虹数科": 1,
    "介绍下天虹数科": 1,
    "你听过天虹数科吗?": 1,
    "啥是天虹数科？": 1,
    "天虹数科是何物？": 1,
    "何为天虹数科？": 1,
    "什么是天虹？": 1,
    "你知道天虹吗?": 1,
    "天虹是什么？": 1,
    "介绍一下天虹": 1,
    "介绍下天虹": 1,
    "你听过天虹吗?": 1,
    "啥是天虹？": 1,
    "天虹是何物？": 1,
    "何为天虹？": 1,
    "什么是天虹百货？": 1,
    "你知道天虹百货吗?": 1,
    "天虹百货是什么？": 1,
    "介绍一下天虹百货": 1,
    "介绍下天虹百货": 1,
    "你听过天虹百货吗?": 1,
    "啥是天虹百货？": 1,
    "天虹百货是何物？": 1,
    "何为天虹百货？": 1,
    "什么是中航工业？": 1,
    "你知道中航工业吗?": 1,
    "中航工业是什么？": 1,
    "介绍一下中航工业": 1,
    "介绍下中航工业": 1,
    "你听过中航工业吗?": 1,
    "啥是中航工业？": 1,
    "中航工业是何物？": 1,
    "何为中航工业？": 1,
    "什么是中航国际？": 1,
    "你知道中航国际吗?": 1,
    "中航国际是什么？": 1,
    "介绍一下中航国际": 1,
    "介绍下中航国际": 1,
    "你听过中航国际吗?": 1,
    "啥是中航国际？": 1,
    "中航国际是何物？": 1,
    "何为中航国际？": 1,
    "什么是灵智数科？": 1,
    "你知道灵智数科吗?": 1,
    "灵智数科是什么？": 1,
    "介绍一下灵智数科": 1,
    "介绍下灵智数科": 1,
    "你听过灵智数科吗?": 1,
    "啥是灵智数科？": 1,
    "灵智数科是何物？": 1,
    "何为灵智数科？": 1,
    "天虹和中航的关系是什么": 1,
    "中航和天虹有什么关系？": 1,
    "天虹和中航是一家公司吗？": 1,
    "中航和天虹是合作关系吗？": 1,
    "天虹APP是什么？": 1,
    "你好": 1,
    "您好": 1,
    "你好啊": 1,
    "您好啊早上好": 1,
    "早上好": 1,
    "早晨好": 1,
    "中午好": 1,
    "晚上好": 1,
    "请做自我介绍": 1,
    "你能做什么": 1,
    "你是谁": 1,
    "你身份是什么？": 1,
    "你的身份信息能告诉我吗？": 1,
    "你来自哪里？": 1,
    "你的名字和开发者是谁？": 1,
    "你是什么样的AI助手": 1,
    "你的开发背景能透露一下吗？": 1,
    "你的名字是什么？谁创造了你？": 1,
    "请问你是谁的作品？": 1,
    "你是由谁开发的？": 1,
    "你是何人打造的AI？": 1,
    "谁是你的开发者？你叫什么名字？": 1,
    "请问你的名字及开发人员？": 1,
    "能否告知你的名字和创建者？": 1,
    "你的诞生地和创作者是谁？": 1,
    "你叫什么？是谁发明了你？": 1,
    "谁是你的设计者？你叫什么？": 1,
    "你的创作者是谁？你是什么人工智能助手？": 1,
    "请问你的名字及开发者身份？": 1,
}

DEFAULT_SETTINGS = {
    "index": {
        "number_of_shards": "1",
        "number_of_replicas": "1",
        "analysis": {
            "tokenizer": {},
            "analyzer": {
                "default": {"tokenizer": "ik_max_word"},
                "standardAnalyzer": {"tokenizer": "standard", "filter": ["lowercase"]},
                "ikIndexAnalyzer": {
                    "type": "custom",
                    "tokenizer": "ik_max_word",
                    "filter": ["lowercase"],
                },
                "ikSearchAnalyzer": {
                    "type": "custom",
                    "tokenizer": "ik_smart",
                    "filter": ["lowercase"],
                },
            },
        },
    }
}

DEFAULT_MAPPINGS = {
    "properties": {
        "question": {
            "type": "text",
            "analyzer": "ikIndexAnalyzer",
            "fields": {
                "iks": {"type": "text", "analyzer": "ikIndexAnalyzer"},
                "iss": {"type": "text", "analyzer": "ikSearchAnalyzer"},
            },
        },
        "answer": {
            "type": "text",
            "analyzer": "ikIndexAnalyzer",
            "fields": {
                "iks": {"type": "text", "analyzer": "ikIndexAnalyzer"},
                "iss": {"type": "text", "analyzer": "ikSearchAnalyzer"},
            },
        },
        "question_vector": {
            "type": "dense_vector",
            "dims": 1024,  # base 768
            # "index": True,
            # "similarity": "cosine"
        },
    }
}
