# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2025/05/13 09:53:01
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''

import sys

sys.path.append("./")

from functools import wraps

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