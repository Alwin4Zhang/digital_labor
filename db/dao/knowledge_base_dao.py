import os
import sys
import re
import uuid
from typing import Dict, List

sys.path.append("./")

from db.session import with_session
from db.models.knowledge_base_model import KnowledgeBaseModel, DocumentBaseModel

from db.models.enum import ReleaseStatus


@with_session
def add_qa_to_db(
    session,
    question,
    answer,
    document_uuid,
    type,
    source=None,
    chunk_index=None,
    created_by=None,
    created_name=None,
    answer_markdown=None
):
    # 创建知识库实例
    qa = KnowledgeBaseModel(
        document_uuid=document_uuid,
        question=question,
        answer=answer,
        answer_markdown=answer_markdown,
        question_type=type,
        source=source,
        chunk_index=chunk_index,
        created_by=created_by,
        updated_by=created_by,
        created_name=created_name,
        updated_name=created_name,
    )
    session.add(qa)
    session.commit()
    return qa.id


@with_session
def add_document_to_db(
    session,
    document_uuid,
    name=None,
    document_type=None,
    question_type=None,
    chunks=None,
    created_by=None,
    created_name=None,
    upload_status=None,
    release_status=None,
    domain=None,
    assert_path=None,
    source=None
):
    # 创建文档实例
    doc = (
        session.query(DocumentBaseModel).filter_by(document_uuid=document_uuid).first()
    )
    if not doc:
        doc = DocumentBaseModel(
            document_uuid=document_uuid,
            name=name,
            document_type=document_type,
            question_type=question_type,
            created_by=created_by,
            updated_by=created_by,
            created_name=created_name,
            updated_name=created_name,
            source=source
        )
    else:
        if assert_path and doc.assert_path is None:  # 上传文件成功
            doc.assert_path = assert_path
            doc.domain = domain
            doc.upload_status = "success"
        if not assert_path and upload_status:  # 只更新状态上传状态
            doc.upload_status = upload_status
        if release_status:  # 更新发布状态
            doc.release_status = release_status
        if chunks:  # 更新文本块json
            doc.chunks = chunks
            if not release_status:
                # doc.release_status = "learning"
                doc.release_status = ReleaseStatus.PARSE_SUCCEED # 解析完成

    session.add(doc)
    session.commit()
    return doc.document_uuid


@with_session
def update_qa_by_id(session, id, question, answer, release_status, chunk_index=None):
    qa = session.query(KnowledgeBaseModel).filter_by(id=id).first()
    if qa.question != question:
        qa.question = question
    if qa.answer != answer:
        qa.answer = answer
    if qa.chunk_index != chunk_index:
        qa.chunk_index = chunk_index
    if qa.release_status != release_status:
        qa.release_status = release_status
    session.add(qa)
    session.commit()
    return qa.id


@with_session
def list_qas_from_db(session, _type, source=None):
    if _type and source:
        qas = (
            session.query(KnowledgeBaseModel)
            .filter_by(question_type=_type, source=source)
            .all()
        )
    elif _type and source is None:
        qas = session.query(KnowledgeBaseModel).filter_by(question_type=_type).all()
    elif source and _type is None:
        qas = session.query(KnowledgeBaseModel).filter_by(source=source).all()
    qas = [qa.to_dict() for qa in qas]
    return qas


@with_session
def delete_qa_from_db(session, id: int):
    qa = session.query(KnowledgeBaseModel).filter_by(id=id).first()
    if qa:
        session.delete(qa)
    return True


@with_session
def get_qa_detail(session, id: int) -> dict:
    qa: KnowledgeBaseModel = session.query(KnowledgeBaseModel).filter_by(id=id).first()
    if qa:
        return qa.to_dict()
    else:
        return {}


@with_session
def get_document_state(session, document_uuid: str) -> dict:
    doc: DocumentBaseModel = (
        session.query(DocumentBaseModel).filter_by(document_uuid=document_uuid).first()
    )
    if doc:
        return doc.release_status


@with_session
def get_documents_state(session, document_uuids: List[str]) -> List[str]:
    """根据若干document uuids获取"""
    query_filter = []
    query_filter.append(DocumentBaseModel.document_uuid.in_(document_uuids))
    docs: DocumentBaseModel = session.query(DocumentBaseModel).filter(*query_filter)
    if docs:
        return [
            {"document_uuid": doc.document_uuid, "release_status": doc.release_status}
            for doc in docs
        ]


@with_session
def get_document_detail(session, document_uuid: int) -> dict:
    doc: DocumentBaseModel = (
        session.query(DocumentBaseModel).filter_by(document_uuid=document_uuid).first()
    )
    if doc:
        return doc.to_dict()
    
@with_session
def get_document_chunks(session,document_uuid: int) -> dict:
    rtuples = session.query(DocumentBaseModel.chunks,DocumentBaseModel.document_uuid).filter_by(document_uuid=document_uuid).first()
    if rtuples:
        return {
            "chunks": rtuples[0]
        }


if __name__ == "__main__":
    uuids = [
        "905c5746b06611ee86f46705253b7244",
        "67395648b45811ee86f46705253b7244",
        "2f6175e0b69a11ee86f46705253b7244",
        "f1949ac6b9b911ee86f46705253b7244",
        "3b1d682eb9c111ee86f46705253b7244",
    ]

    # print(get_documents_state(uuids))
    import time
    document_uuid = "e34a43964e4511ef86f46705253b7244"
    start = time.time()
    get_document_chunks(document_uuid)
    print(time.time() - start)
