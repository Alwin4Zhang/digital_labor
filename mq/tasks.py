import io
import time
# from celery import shared_task
# from fastapi import Body,UploadFile,File,Request
from db.models.enum import FileSource
from mq.celery_app import celery_app
from db.service.knowledge_base_service import upload_file_task,parse_document_to_db,qa_generate_to_db,add_document_to_db,parse_doc_file_with_stream
from loader.unstructured_loaders.pdf_loader import PDFLoader

from configs.apollo_config import logger

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task
def create_upload_file_task(
    question_type,
    created_by,
    created_name,
    source: str ,
    file_name: str,
    file_stream: None
):
    """创建上传文件任务,并返回uuid"""
    document_uuid = upload_file_task(
        file_name=file_name,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
        source=source
    )
    logger.info(f"上传文件接口，上传文件:{file_name}，问题类型:{question_type}，创建人:{created_name}")

    pdf_loader = PDFLoader(file_path=file_name,file_stream=file_stream)
    logger.info(pdf_loader.blocks)

    # res, file_type = parse_doc_file_with_stream(
    #     file_name=file_name, file_stream=file_stream, source=source
    # )
    # logger.info(f"{res} - {file_type}")
    # document_uuid=parse_document_to_db(
    #     document_uuid=document_uuid,
    #     file_name=file_name,
    #     file_stream=file_stream,
    #     source=source,
    #     question_type=question_type,
    #     created_by=created_by,
    #     created_name=created_name,
    #     sprag_enhance=True
    # )
    return {
        "status": "success",
        "document_uuid": document_uuid
    }