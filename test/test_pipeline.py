import os
import io
import sys
import re
import time
import uuid
import json
import shutil
import math
import logging
from typing import Dict, List
from io import BytesIO, StringIO

sys.path.append("./")

from configs.apollo_config import logger



from db.service.knowledge_base_service import (
    upload_file_task,
    parse_document_to_db,
    parse_doc_file_with_stream,
    qa_generate_to_db,
)


def test_pipeline(
    doc_path,
    file_name: str = None,
    source="文件上传",
    question_type="人力",
    created_by=157212,
    created_name="张三",
    task_type=None
):
    with open(doc_path, "rb") as rf:
        file_stream = BytesIO(rf.read())
    document_uuid = upload_file_task(
        file_name=doc_path,
        question_type="pdf",
        created_by=created_by,
        created_name=created_name
    )
    print(document_uuid)
    logger.info(f"insert document {document_uuid} success!")


    document_uuid = parse_document_to_db(
        document_uuid=document_uuid,
        file_name=file_name,
        file_stream=file_stream,
        source=source,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
        sprag_enhance=True,
        task_type=task_type
    )

    qa_ids = qa_generate_to_db(document_uuid=document_uuid,
                               source=source,
                               question_type=question_type,
                               created_by=created_by,
                               created_name=created_name)
    print(qa_ids)
    return document_uuid


if __name__ == "__main__":

    source = "文件上传"
    question_type = "人力"
    created_by = 157000
    created_name = "张三"

    file_name = "9.6.3.0.2 交通补贴发放规范.docx"
    doc_path = f"././test/test_files/{file_name}"
    
    # doc_path = "/Users/ucdteam/digital_labor/test/test_files/操作教程.pdf"
    test_pipeline(doc_path, 
                  file_name,
                  source, question_type, created_by, created_name,
                  task_type="document"
                  )
