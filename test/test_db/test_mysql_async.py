import sys
import pytest
import aiomysql
import asyncio

sys.path.append("././")
from db.mysql.session import with_session
from db.models.knowledge_base_model import KnowledgeBaseModel, DocumentBaseModel
from sqlalchemy import select

from utils.common import timeit
from configs.apollo_config import SQLALCHEMY_DATABASE_URI

from db.dao.dialogue_history_dao import (
    add_dialogue_history_to_db,
    get_dialogue_history_by_id,
    filter_dialogue_history,
)

from db.dao.knowledge_base_dao import (
    add_qa_to_db,
    add_document_to_db,
    update_qa_by_id,
    list_qas_from_db,
    delete_qa_from_db,
    get_qa_detail,
    get_document_state,
    get_documents_state,
    get_document_detail,
    get_document_chunks,
)


# @timeit
# @with_session
# async def list_qas_from_db(session, _type=None, source=None):
#     q = select(KnowledgeBaseModel).where(KnowledgeBaseModel.question_type == _type)
#     result = await session.execute(q)
#     return result.scalars().all()


@timeit
@with_session
async def test2(session, _type=None, source=None):
    # session = get_db()
    statement = select(KnowledgeBaseModel).where(
        KnowledgeBaseModel.question_type == _type
    )
    result = await session.execute(statement)
    # result = (
    #     await session.query(KnowledgeBaseModel).filter_by(question_type=_type).all()
    # )
    return result.scalars().all()
    # qas = await list_qas_from_db(session, _type=_type, source=source)


if __name__ == "__main__":

    # qas = test2(_type="人力")
    # print(qas)

    import time

    start_time = time.time()
    r = asyncio.run(test2(_type="人力"))
    print(r)

    # 插入数据
    # r = asyncio.run(
    #     add_dialogue_history_to_db(chat_type="QA", query="你是谁", response="我是小天")
    # )
    # print(r)

    # 过滤对话记录
    # r = asyncio.run(get_dialogue_history_by_id(dialog_history_id=18))
    # print(r)

    # 查询聊天记录
    # r = asyncio.run(filter_dialogue_history(query="你是"))
    # print(r)

    # 添加qa
    # start = time.time()
    # r = asyncio.run(
    #     add_qa_to_db(
    #         question="你是谁",
    #         answer="我是小天",
    #         document_uuid="1234567890",
    #         type="人力",
    #     )
    # )
    # print(r, time.time() - start)

    # 删除QA
    # r = asyncio.run(delete_qa_from_db(id=30367))
    # print(r)

    # 查询QA
    # r = asyncio.run(get_qa_detail(id=30366))
    # print(r)

    # 查询qas
    # r = asyncio.run(list_qas_from_db(_type="人力"))
    # print(r)

    # 更新qa
    # r = asyncio.run(
    #     update_qa_by_id(
    #         id=30366,
    #         question="你是谁",
    #         answer="我是小天",
    #         release_status="qa_await",
    #     )
    # )
    # print(r)

    # 添加文档
    # r = asyncio.run(
    #     add_document_to_db(
    #         document_uuid="6a73d5e865b711efb5e10242ac1100056",
    #         name="测试文档123",
    #         document_type="文档类型123",
    #         question_type="人力",
    #         chunks={},
    #         created_by="张三",
    #         upload_status="upload_success",
    #     )
    # )
    # print(r)

    # 查询文档
    # r = asyncio.run(
    #     get_document_state(document_uuid="6a73d5e865b711efb5e10242ac110005")
    # )
    # print(r)

    # 查询文档chunks
    # r = asyncio.run(
    #     get_document_chunks(document_uuid="6a73d5e865b711efb5e10242ac110005")
    # )
    # print(r)
