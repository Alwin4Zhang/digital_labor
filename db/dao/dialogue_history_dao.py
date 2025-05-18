import os
import sys
import re
import uuid
from typing import Dict, List

sys.path.append("./")

from db.session import with_session
from db.models.dialogue_history_model import DialogueBaseModel


def _convert_query(query: str) -> str:
    p = re.sub(r"\s+", "%", query)
    return f"%{p}%"


@with_session
def add_dialogue_history_to_db(
    session, chat_type, query, response="", meta_data: Dict = {}
):
    """新增聊天记录"""
    # if not dialog_history_id:
    #     dialog_history_id = uuid.uuid1().hex

    dh = DialogueBaseModel(
        chat_type=chat_type, query=query, response=response, meta_data=meta_data
    )

    session.add(dh)
    session.commit()
    return dh.id


@with_session
def get_dialogue_history_by_id(session, dialog_history_id) -> DialogueBaseModel:
    """查询聊天记录"""
    dh = session.query(DialogueBaseModel).filter_by(id=dialog_history_id).first()
    return dh


@with_session
def filter_dialogue_history(session, query=None, response=None) -> DialogueBaseModel:
    """查询聊天记录"""
    dh = session.query(DialogueBaseModel)
    if query is not None:
        dh = dh.filter(DialogueBaseModel.query.ilike(_convert_query(query))).all()
    if response is not None:
        dh = dh.filter(DialogueBaseModel.response.ilike(_convert_query(response))).all()
    return dh
