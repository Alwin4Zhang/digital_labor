# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2025/05/13 09:53:01
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''

import sys

sys.path.append("./")

from functools import wraps

# import langfuse
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

from configs.apollo_config import LANGFUSE_HOST,LANGFUSE_PK,LANGFUSE_SK


langfuse = Langfuse(
    secret_key=LANGFUSE_SK,
    public_key=LANGFUSE_PK,
    host=LANGFUSE_HOST,
)

langfuse_handler = CallbackHandler(
    secret_key=LANGFUSE_SK,
    public_key=LANGFUSE_PK,
    host=LANGFUSE_HOST,
    metadata={
        "provider": "lingzhi",
    }
)

# across_intent_prompt = langfuse_h.get_prompt("across_intent_prompt")
# print(across_intent_prompt)