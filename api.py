import argparse
import json
import os
import shutil
import uuid
# import logging
import io
from typing import List, Optional, Dict

import asyncio
import pydantic
import uvicorn
from fastapi import (
    Body,
    FastAPI,
    File,
    Form,
    Query,
    UploadFile,
    WebSocket,
    Request,
    APIRouter,
    BackgroundTasks,
)
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import UploadFile
from pydantic import BaseModel
from tqdm import tqdm

from chains.local_rag import LocalRAG
from chains.local_chunk_rag import LocalChunkRAG
from chains.local_hybrid_rag import LocalHybridRag
from configs.model_config import (
    KB_ROOT_PATH,
    EMBEDDING_DEVICE,
    EMBEDDING_MODEL,
    VECTOR_SEARCH_TOP_K,
    LLM_HISTORY_LEN,
    OPEN_CROSS_DOMAIN,
    DEFAULT_NULL_RESPONSE,
    DEFAULT_RESPONSE
)
from configs.apollo_config import logger

from db.service.knowledge_base_service import (
    parse_doc_file_with_stream,
    upload_file_task,
    parse_document_to_db,
    qa_generate_to_db,
    # get_document_detail,
    # get_document_state
)

from db.dao.knowledge_base_dao import (
    get_document_state,
    get_documents_state,
    get_document_detail,
)
from db.service.milvus_kb_service import default_vector_db
from db.service.milvus_chunk_db_service import default_chunk_db
from db.service.elasticsearch_kb_service import default_es_db
from db.service.knowledge_base_service import qa_release_valiate
from db.embedding_utils import embed_texts_api
from db.models.enum import FileSource
from concurrent.futures import ProcessPoolExecutor
from utils.util_logger import logger

from utils.service_trace import request_id_context


class ConnectionManager:
 
    def __init__(self):
        """存放链接"""
        self.active_connections: List[Dict[str, WebSocket]] = []
 
    async def connect(self, ws: WebSocket):
        """链接"""
        self.active_connections.append({"ws": ws})
 
    async def disconnect(self, ws: WebSocket):
        """断开链接，移除"""
        self.active_connections.remove({"ws": ws})
        

ws_manager = ConnectionManager()

local_doc_rag = LocalRAG()

local_doc_chunk_rag = LocalChunkRAG()

local_hybrid_rag = LocalHybridRag()


class BaseResponse(BaseModel):
    code: int = pydantic.Field(200, description="HTTP status code")
    msg: str = pydantic.Field("success", description="HTTP status message")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
            }
        }


class ListDocsResponse(BaseResponse):
    data: List[str] = pydantic.Field(..., description="List of document names")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": ["doc1.docx", "doc2.pdf", "doc3.txt"],
            }
        }


class StringResponse(BaseResponse):
    data: str = pydantic.Field(..., description="custom string data")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": "abc",
            }
        }


class ListDocsContentResponse(BaseResponse):
    data: List[dict] = pydantic.Field(..., description="List of document json content")

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [
                    {"knowledge_id": 1, "question": "你是谁", "answer": "我是小天"},
                    {
                        "knowledge_id": 2,
                        "question": "你是哪位",
                        "answer": "我是小天，灵智数科智能助手",
                    },
                ],
            }
        }


class ListDocsEmbedResponse(BaseResponse):
    data: List[List[dict]] = pydantic.Field(
        ..., description="List of document json content"
    )

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [
                    [{"knowledge_id": 1, "question": "你是谁", "answer": "我是小天"}],
                    [
                        {
                            "knowledge_id": 2,
                            "question": "你是哪位",
                            "answer": "我是小天，灵智数科智能助手",
                        }
                    ],
                ],
            }
        }


class ListEmbedResponse(BaseResponse):
    data: List[List[float]] = pydantic.Field(
        ..., description="List of document json content"
    )

    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "success",
                "data": [
                    [0.1, 0.2, 0.3],
                    [0.1, 0.2, 0.4],
                ],
            }
        }


async def stream_ws_chat(websocket: WebSocket):
    await websocket.accept()
    turn = 1
    while True:
        input_json = await asyncio.wait_for(websocket.receive_json(), 60)
        question, history = input_json["question"], input_json.get("history", [])
        is_append = input_json.get("is_append", True)
        print(f"current question:{question},current history:{history}")
        for resp, history in local_doc_rag.get_knowledge_based_answer_multi_round(
            query=question, chat_history=history, is_append=is_append
        ):
            await asyncio.sleep(0)
            await websocket.send_json(
                {
                    "response": resp["result"],
                    "type": resp["type"],
                    "history": history,
                    "status": 202,
                }
            )
            # last_print_len = len(resp["result"])

        source_documents = []

        for inum, doc in enumerate(resp["source_documents"]):
            is_source = 0
            if inum == 0:
                is_source = 1
            source_documents.append(
                {
                    "url": doc.get("url", ""),
                    "title": doc.get("question"),
                    "is_source": is_source,
                }
            )

        await websocket.send_json(
            {
                "knowledge_id": resp.get("knowledge_id"),
                "response": resp["result"],
                "type": resp["type"],
                "history": history,
                "status": 202,
                "source_documents": source_documents,
            }
        )
        await websocket.send_json({"status": 200})


async def suggest(request: Request):
    body = await request.json()
    query = body.get("query", "")
    hits = default_es_db.suggest(query=query)
    hits = [hit["_source"]["question"] for hit in hits]
    return ListDocsResponse(data=hits)


async def show_document_state(request: Request):
    body = await request.json()
    document_uuid = body.get("document_uuid")
    release_status = get_document_state(document_uuid)
    if release_status:
        logger.info(f"current document state:\t{release_status}")
        return StringResponse(data=release_status)
    else:
        file_status = "未查到该文档"
        return StringResponse(code=500, msg=file_status, data="")


async def show_documents_state(request: Request):
    """批量查询文档状态"""
    body = await request.json()
    document_uuids = body.get("document_uuids", [])
    # 优化sql查询，一条查询条件查看所有结果
    document_stats = get_documents_state(document_uuids=document_uuids)
    logger.info(f"current documents state:\t{document_stats}")
    if document_stats:
        return ListDocsContentResponse(data=document_stats)
    else:
        file_status = "查询出错"
        return ListDocsContentResponse(code=500, msg=file_status, data=[])


async def create_upload_file(
    background_tasks: BackgroundTasks,
    question_type: str = Body(..., description="问题类型", example="人力"),
    created_by: str = Body(..., description="创建人工号", example="157212"),
    created_name: str = Body(..., description="创建人姓名", example="张三"),
    source: str = Body(description="任务类型-文件解析or知识问答", default=FileSource.Document),
    file: UploadFile = File(),
    sprag_enhance: bool = Body(description="是否开启sprag", default=True),
    request: Request = None
):
    """创建上传文件任务,并返回uuid"""
    file_name = file.filename
    file_stream = io.BytesIO(await file.read())
    await file.close()
    document_uuid = upload_file_task(
        file_name=file_name,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
        source=source
    )
    
    logger.info(f"上传文件接口，上传文件:{file_name}，问题类型:{question_type}，创建人:{created_name}")

    logger.info(request.headers.get("x-b3-traceid"))
    # 添加后台任务
    # 任务1 解析文档
    background_tasks.add_task(
        parse_document_to_db,
        document_uuid=document_uuid,
        file_name=file_name,
        file_stream=file_stream,
        source=source,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
        sprag_enhance=sprag_enhance,
        trace_id=request.headers.get("x-b3-traceid")
    )
    # 任务2 生成qa对
    # background_tasks.add_task(
    #     qa_generate_to_db,
    #     document_uuid=document_uuid,
    #     source=source,
    #     question_type=question_type,
    #     created_by=created_by,
    #     created_name=created_name,
    # )
    return StringResponse(data=document_uuid)


async def create_upload_files(
    background_tasks: BackgroundTasks,
    question_type: str = Body(..., description="问题类型", example="人力"),
    created_by: str = Body(..., description="创建人工号", example="157212"),
    created_name: str = Body(..., description="创建人姓名", example="张三"),
    files: List[UploadFile] = File(description="Multiple files as UploadFile"),
    sprag_enhance: bool = Body(description="是否开启sprag", default=True),
    source: str = Body(description="任务类型", default=FileSource.Document),
    request: Request = None
):
    """创建批量上传文件任务,并返回uuids"""
    document_res = []
    for file in tqdm(files):
        try:
            file_name = file.filename
            file_stream = io.BytesIO(await file.read())
            await file.close()

            document_uuid = upload_file_task(
                file_name=file_name,
                question_type=question_type,
                created_by=created_by,
                created_name=created_name,
                source=source
            )
            document_res.append(
                {"document_uuid": document_uuid, "file_name": file_name}
            )

            if sprag_enhance is None:
                sprag_enhance = False
            # 任务1 解析文档

            # 添加后台任务
            # 任务1 解析文档
            background_tasks.add_task(
                parse_document_to_db,
                document_uuid=document_uuid,
                file_name=file_name,
                file_stream=file_stream,
                source=source,
                question_type=question_type,
                created_by=created_by,
                created_name=created_name,
                sprag_enhance=sprag_enhance,
                trace_id=request.headers.get("x-b3-traceid")
            )
            # 任务2 生成qa对
            # background_tasks.add_task(
            #     qa_generate_to_db,
            #     document_uuid=document_uuid,
            #     source=source,
            #     question_type=question_type,
            #     created_by=created_by,
            #     created_name=created_name,
            # )
        except Exception as e:
            logger.error(f"create_upload_files error: {e}")
    
    file_names = '\n'.join([file.filename for file in files])
    logger.info(f"批量上传文件接口，上传文件:{file_names}，问题类型:{question_type}，创建人:{created_name}")

    return ListDocsContentResponse(data=document_res)


async def create_qas_from_file(
    background_tasks: BackgroundTasks,
    document_uuid: str = Body(..., description="文档uuid", example="157212"),
    source: str = Body(description="任务类型", default=FileSource.KnowledgeQA),
    question_type: str = Body(..., description="问题类型", example="人力"),
    created_by: str = Body(..., description="创建人工号", example="157212"),
    created_name: str = Body(..., description="创建人姓名", example="张三"),
):
    """生成问答对"""
    background_tasks.add_task(
        qa_generate_to_db,
        document_uuid=document_uuid,
        source=source,
        question_type=question_type,
        created_by=created_by,
        created_name=created_name,
    )
    
    logger.info(f"问答对入库,上传文件uuid:{document_uuid},问题类型:{question_type},创建人:{created_name}")
    return StringResponse(data=document_uuid)


async def create_qas_from_files(
    background_tasks: BackgroundTasks,
    document_uuids: List[str] = Body(
        ..., description="文档uuids", example=["157212", "157213"]
    ),
    source: str = Body(..., description="来源", example="上传"),
    question_type: str = Body(..., description="问题类型", example="人力"),
    created_by: str = Body(..., description="创建人工号", example="157212"),
    created_name: str = Body(..., description="创建人姓名", example="张三"),
):
    """批量文档发布，生成问答对"""
    for document_uuid in document_uuids:
        background_tasks.add_task(
            qa_generate_to_db,
            document_uuid=document_uuid,
            source=source,
            question_type=question_type,
            created_by=created_by,
            created_name=created_name,
        )
    logger.info(f"批量发布文件，生成QA对,上传文件uuids:{document_uuids},来源:{source},问题类型:{question_type},创建人:{created_name}")
    return ListDocsResponse(data=document_uuids)



async def add_docs_to_vector_db(docs: List[dict] = None):
    """添加文档到索引库"""
    logger.info("add docs to vector dbs:\t", docs)
    pks = default_vector_db.add_doc(docs=docs)
    return ListDocsResponse(data=pks)


async def delete_docs_from_vector_db(docs: List[dict] = None):
    """从索引库删除文档"""
    logger.info("delete docs from vector dbs:\t", docs)
    pks = default_vector_db.delete_doc(docs=docs)
    return ListDocsResponse(data=pks)


async def update_docs_to_vector_db(docs: List[dict] = None):
    """在索引库更新文档"""
    logger.info("update docs from vector dbs:\t", docs)
    pks = default_vector_db.update_doc(docs=docs)
    return ListDocsResponse(data=pks)


async def add_docs_to_es_db(docs: List[dict] = None):
    """添加文档到es索引库"""
    logger.info("add docs to elastisearch dbs:\t", docs)
    ids = default_es_db.add_doc(docs=docs)
    return ListDocsResponse(data=ids)


async def delete_docs_from_es_db(docs: List[dict] = None):
    """从es索引库删除文档"""
    logger.info("delete docs from elasticsearch dbs:\t", docs)
    ids = default_es_db.delete_doc(docs=docs)
    return ListDocsResponse(data=ids)


async def update_docs_to_es_db(docs: List[dict] = None):
    """在es索引库更新文档"""
    logger.info("update docs from elastisearch dbs:\t", docs)
    ids = default_es_db.update_doc(docs=docs)
    return ListDocsResponse(data=ids)


async def delete_qas(docs: List[dict] = None):
    """删除qa对,同时删除es索引库和milvus索引库"""
    logger.info("delete docs from vector dbs:\t", docs)
    pks = default_vector_db.delete_doc(docs=docs)
    logger.info("delete docs from elasticsearch dbs:\t", docs)
    ids = default_es_db.delete_doc(docs=docs, field="knowledge_id")
    return ListDocsResponse(data=pks + ids)


async def delete_doc(docs: List[dict] = None):
    """删除qa对，同时删除es索引库、milvus qa索引、chunk索引"""
    # 删除qa对索引
    logger.info("delete docs from vector dbs:\t", docs)
    pks = default_vector_db.delete_doc(docs=docs)
    # 删除chunk索引
    chunk_pks = default_chunk_db.delete_doc(docs=docs)
    # 删除es索引
    logger.info("delete docs from elasticsearch dbs:\t", docs)
    ids = default_es_db.delete_doc(docs=docs, field="knowledge_id")
    return ListDocsResponse(data=pks + chunk_pks + ids)


async def qa_release_validate(docs: List[dict] = None):

    def inner_validate(docs, threshold=90):
        from fuzzywuzzy import fuzz

        inner_res = []
        rest_docs = []
        while docs:
            cur_doc = docs.pop(0)
            rest_docs.append(cur_doc)
            cur_id = cur_doc.get("id")
            cur_q = cur_doc.get("question")
            tp_similar_question = []
            for d in docs:
                _id = d.get("id")
                dq = d.get("question")
                if not dq:
                    continue
                simi_score = fuzz.ratio(cur_q, dq)
                if simi_score >= threshold:
                    tp_similar_question.append(
                        {
                            "id": str(_id),
                            "question": dq,
                            "score": simi_score,
                            "similar_type": 0,
                        }
                    )
                    docs.remove(d)

            if tp_similar_question:
                inner_res.append(
                    {
                        "id": str(cur_id),
                        "question": cur_q,
                        "similar_questions": tp_similar_question,
                    }
                )
        return inner_res, rest_docs

    res = []
    # TODO: 队列内校验
    inner_res, rest_docs = inner_validate(docs[:])
    logger.info(rest_docs)
    inner_dict = {r["id"]: r for r in inner_res}
    res.extend(inner_res)
    for doc in rest_docs:
        _id = str(doc.get("id"))
        question = doc.get("question")
        if not question:
            continue
        simi_pairs = local_doc_rag.question_validate(question=question)
        similar_questions = [
            {"id": pair[0], "question": pair[1], "score": pair[2], "similar_type": 1}
            for pair in simi_pairs
        ]
        if _id in inner_dict:
            similar_questions = inner_dict[_id]["similar_questions"] + similar_questions
            res.remove(inner_dict[_id])
        if similar_questions:
            res.append(
                {
                    "id": str(_id),
                    "question": question,
                    "similar_questions": similar_questions,
                }
            )

    # questions = []
    # for doc in rest_docs:
    #     question = doc.get("question")
    #     if not question:
    #         continue
    #     questions.append(question)
    # results = local_doc_rag.question_validate_parallel(questions=questions)
    # kvs = {}
    # for i,question,similar_questions in results:
    #     kvs[i] = similar_questions

    # for i,doc in enumerate(rest_docs):
    #     _id = str(doc.get("id"))
    #     question = doc.get("question")
    #     if not question:
    #         continue
    #     simi_pairs = kvs.get(i)
    #     if not simi_pairs:
    #         similar_questions = []
    #     else:
    #         similar_questions = [
    #             {"id": pair[0], "question": pair[1], "score": pair[2], "similar_type": 1}
    #             for pair in simi_pairs
    #         ]
    #     if _id in inner_dict:
    #         similar_questions = inner_dict[_id]["similar_questions"] + similar_questions
    #         res.remove(inner_dict[_id])

    #     if similar_questions:
    #         res.append({
    #             "id": str(_id),
    #             "question": question,
    #             "similar_questions": similar_questions,
    #         })

    return ListDocsContentResponse(data=res)


async def qa_release_hybird_validate(docs: List[dict] = None):
    similar_groups = qa_release_valiate(docs=docs)
    return ListDocsEmbedResponse(data=similar_groups)


async def stream_ws_chunk_chat(websocket: WebSocket):
    await websocket.accept()
    turn = 1
    while True:
        input_json = await websocket.receive_json()
        # input_json = await asyncio.wait_for(websocket.receive_json(), 90)
        question, history = input_json["question"], input_json.get("history", [])
        is_append = input_json.get("is_append", True)
        print(f"current question:{question},current history:{history}")

        await websocket.send_json({"question": question, "turn": turn, "flag": "strt"})

        for resp, history in local_doc_chunk_rag.dialog_onetune(
            query=question, chat_history=history, is_append=is_append
        ):
            await asyncio.sleep(0)
            await websocket.send_json(
                {
                    "response": resp["result"],
                    "type": resp["type"],
                    "history": history,
                    "status": 202,
                }
            )
            # last_print_len = len(resp["result"])

        source_documents = []

        for inum, doc in enumerate(resp["source_documents"]):
            # is_source = 0
            doc["is_source"] = 0
            if inum == 0:
                # is_source = 1
                doc["is_source"] = 1
            source_documents.append(
                # {
                #     "url": doc.get("url", ""),
                #     "title": doc.get("title"),
                #     "is_source": is_source,
                # }
                doc
            )

        await websocket.send_json(
            {
                "knowledge_id": resp.get("knowledge_id"),
                "response": resp["result"],
                "type": resp["type"],
                "history": history,
                "status": 202,
                "source_documents": source_documents,
            }
        )
        await websocket.send_json({"status": 200})


async def stream_ws_hybrid_chat(websocket: WebSocket):
    """
    流式混合搜索
    TODO: 需要兼容文档内容过长，输入大模型超长的问题
    """
    await websocket.accept()
    # get traceid
    trace_id = None
    for header in websocket.headers.raw:
        header_name,header_value = str(header[0],encoding='utf-8'),str(header[1],encoding='utf-8')
        if header_name.lower() == "x-b3-traceid":
            trace_id = header_value
            break
    # get user_id 显性传入

    await ws_manager.connect(websocket)
    try:
        while True:
            input_json = await asyncio.wait_for(websocket.receive_json(), 90)
            question, history = input_json["question"], input_json.get("history", [])
            logger.info(f"current question:{question},current history:{history}")
            created_by = input_json.get("created_by")
            for resp, history in local_hybrid_rag.dialog_onetune(
                query=question, chat_history=history,trace_id=trace_id,created_by=created_by
            ):
                await asyncio.sleep(0)
                await websocket.send_json(
                    {
                        "response": resp["result"],
                        "history": history,
                        "status": 202,
                    }
                )

            # source document表示qas 需要的字段 question,knowledge_id,document_uuid,is_source
            source_documents, required_doc_fields = [], [
                "knowledge_id",
                "question",
                "document_uuid",
                "is_source",
                "chunk_id",
            ]
            # source_files 表示原始文档 需要的字段: filename,document_uuid,is_source 涉及到去重
            source_files, required_file_fields, file_dict = (
                [],
                ["filename", "document_uuid", "is_source"],
                {},
            )

            # 如果返回为空，或者返回没有相关内容，则二次兜底
            total_resp = resp.get("result", "").strip()
            if not total_resp:  # 返回为空，二次兜底,没有相关信息，清空source
                resp["source_documents"] = []
                resp["source_files"] = []
                resp["result"] = DEFAULT_RESPONSE
                history[-1]["content"] = DEFAULT_RESPONSE

            if total_resp == DEFAULT_RESPONSE:  # 返回没有相关信息，清空source
                resp["source_documents"] = []
                resp["source_files"] = []

            for inum, doc in enumerate(resp["source_documents"]):
                doc["is_source"] = 0
                if inum == 0:
                    doc["is_source"] = 1
                source_documents.append(
                    {k: v for k, v in doc.items() if k in required_doc_fields}
                )
                document_uuid = doc.get("document_uuid")
                if document_uuid not in file_dict:
                    source_file = {
                        k: v for k, v in doc.items() if k in required_file_fields
                    }
                    if len(source_file) != len(required_file_fields):
                        continue
                    source_files.append(source_file)
                    file_dict[document_uuid] = len(source_files) - 1

            await websocket.send_json(
                {
                    "knowledge_id": resp.get("knowledge_id"),
                    "response": resp["result"],
                    "history": history,
                    "status": 202,
                    "source_documents": source_documents,
                    "source_files": source_files,
                }
            )
            await websocket.send_json({"status": 200})
    except WebSocketDisconnect as e:
        await ws_manager.disconnect(websocket)


async def search_docs_from_vector_db(request: Request):
    """测试接口，在milvus查询索引"""
    body = await request.json()
    query = body.get("query")
    logger.info(f"do searching docs from vector dbs,search keyword:{query}")
    docs = default_vector_db.do_search(query=query)
    return ListDocsContentResponse(data=docs)


async def embed_texts(request: Request):
    body = await request.json()
    texts = body.get("texts", [])
    if not texts:
        return ListDocsResponse(data=[])
    return ListEmbedResponse(data=embed_texts_api(texts))


def hello_world():
    return StringResponse(data="hello world!")

async def hello_world2(request: Request):
    logger.info(request.headers)
    return StringResponse(data='123')


# def api_start(host, port):

router = APIRouter()
app = FastAPI()

@app.middleware("http")
async def add_request_header(request: Request, call_next):
    # 链路追踪请求id
    request_id = request.headers.get("X-B3-TraceId", str(uuid.uuid4()))
    request_id_context.set(request_id)
    response = await call_next(request)
    response.headers["X-B3-TraceId"] = request_id
    request_id_context.set(None)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router.get("/local_doc_qa/hello_world2", response_model=StringResponse)(hello_world2)

router.websocket("/local_doc_qa/stream_ws_chat")(stream_ws_chat)

router.post("/local_doc_qa/suggest", response_model=ListDocsResponse)(suggest)

# TODO:文件上传相关接口
router.post("/local_doc_qa/create_upload_file_task", response_model=StringResponse)(
    create_upload_file
)

# TODO:批量文件上传相关接口
router.post(
    "/local_doc_qa/create_upload_files_task", response_model=ListDocsContentResponse
)(create_upload_files)

router.post("/local_doc_qa/create_qas_from_file", response_model=StringResponse)(
    create_qas_from_file
)

router.post("/local_doc_qa/create_qas_from_files", response_model=ListDocsResponse)(
    create_qas_from_files
)

router.post("/local_doc_qa/document_state", response_model=StringResponse)(
    show_document_state
)

router.post("/local_doc_qa/document_states", response_model=ListDocsContentResponse)(
    show_documents_state
)

router.post("/local_doc_qa/add_docs_to_vector_db", response_model=ListDocsResponse)(
    add_docs_to_vector_db
)

router.post(
    "/local_doc_qa/delete_docs_from_vector_db", response_model=ListDocsResponse
)(delete_docs_from_vector_db)

router.post("/local_doc_qa/update_docs_to_vector_db", response_model=ListDocsResponse)(
    update_docs_to_vector_db
)

router.post("/local_doc_qa/add_docs_to_es_db", response_model=ListDocsResponse)(
    add_docs_to_es_db
)

router.post("/local_doc_qa/delete_docs_from_es_db", response_model=ListDocsResponse)(
    delete_docs_from_es_db
)

router.post("/local_doc_qa/update_docs_to_es_db", response_model=ListDocsResponse)(
    update_docs_to_es_db
)

router.post(
    "/local_doc_qa/qa_release_validate", response_model=ListDocsContentResponse
)(qa_release_validate)

router.post(
    "/local_doc_qa/qa_release_hybird_validate", response_model=ListDocsEmbedResponse
)(qa_release_hybird_validate)

router.post(
    "/local_doc_qa/search_docs_from_vector_db", response_model=ListDocsContentResponse
)(search_docs_from_vector_db)

router.post("/local_doc_qa/delete_qas", response_model=ListDocsResponse)(delete_qas)

router.post("/local_doc_qa/delete_doc", response_model=ListDocsResponse)(delete_doc)

router.get("/local_doc_qa/hello", response_model=StringResponse)(hello_world)

router.websocket("/local_doc_qa/stream_ws_chunk_chat")(stream_ws_chunk_chat)

router.websocket("/local_doc_qa/stream_ws_hybrid_chat")(stream_ws_hybrid_chat)

router.post("/local_doc_qa/embeded_texts", response_model=ListEmbedResponse)(
    embed_texts
)

app.include_router(router, prefix="/api/rainbow")
# uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog='AI数字员工',
    description='AI数字员工项目')
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7861)
    # 初始化消息
    # args = None
    args = parser.parse_args()
    # api_start(args.host, args.port)

    uvicorn.run(app,
                host=args.host,
                port=args.port)

    # uvicorn.run("api:app", host=args.host, port=args.port, workers=5)
