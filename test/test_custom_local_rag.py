# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2023/07/12 13:45:32
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''

import os
import sys

sys.path.append("././")

from chains.local_rag import LocalRAG
from chains.local_chunk_rag import LocalChunkRAG

# local_rager = LocalRAG()

# q = "中国工厂当成立于哪一年?"

# local_rager.get_knowledge_based_answer_multi_round(query=q)

local_chunk_rager = LocalChunkRAG()

content = local_chunk_rager.dialog_onetune(query="顾客无法联系 订单二次配送",
                                           is_append=True)

for c in content:
    print(c)
