# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2024/01/03 15:40:45
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''

import sys
import json

sys.path.append('./')

from db.dao.dialogue_history_dao import add_dialogue_history_to_db, get_dialogue_history_by_id, filter_dialogue_history
from db.dao.knowledge_base_dao import add_qa_to_db, add_document_to_db, update_qa_by_id, list_qas_from_db, delete_qa_from_db, get_qa_detail

from db.base import Base, create_engine, engine

# TODO:获取账户信息的需要更改
# user = "root"
# pwd = "123456"
# host = "10.60.236.245"
# db = "langchain_llm"

# engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{host}/{db}",
#                        json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),)

# Base.metadata.create_all(bind=engine)

# TODO:验证dialogue history model
# 添加对话记录
# add_dialogue_history_to_db(chat_type='llm',
#                            query="你是谁",
#                            response='我是小天',
#                            meta_data={
#                                "name": 'zs',
#                                "gender": 'male'
#                            })

# 查询对话记录
# dh = get_dialogue_history_by_id(dialog_history_id=1)
# print(dh)

# 模糊查询
# filter_dialogue_history(query="你是谁")
# dh = filter_dialogue_history(response="我是小天")

# print(dh)

# TODO:验证knowledge base model
# 插入知识库
# qa = add_qa_to_db(question='你是哪位啊',
#                   answer='我是小天啊',
#                   document_uuid='1234567',
#                   type='运维',
#                   kb_name='sas')

# 插入文档库
# doc_id = add_document_to_db(id="12345678",
#                    file_name='test.docx',
#                    file_type='docx',
#                    kb_name='sas')
# print(doc_id)

# 更新知识库
# qa_id = update_qa_by_id(
#   id=1,
#   question='你是哪个啊',
#   answer='我是小天，你的专属助理',
#   chunk_index=1,
#   release_status="release"
# )
# print(qa_id)

# 删除知识库数据
# print(delete_qa_from_db(id=2))

# 查询qa详情
# qa = get_qa_detail(id=1)
# print(qa)

# q = "你是谁"
# a = "我是小天"

# document_uuid = "12345678"
# _type = "人力"
# add_qa_to_db(
#   question=q,
#   answer=a,
#   document_uuid=document_uuid,
#   type=_type
# )