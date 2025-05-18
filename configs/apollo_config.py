import os
import sys
# import logging

sys.path.append("./")

from utils.util_logger import logger

# milvus configurations
MILVUS_HOST = "127.0.0.1"
MILVUS_PORT = "19530"
MILVUS_USERNAME = None
MILVUS_PASSWORD = None

# logger info
# logging.info(f"current milvus host:{MILVUS_HOST};milvus port:{MILVUS_PORT};milvus_user:{MILVUS_USERNAME};milvus_password:{MILVUS_PASSWORD}")

# elasticsearch configurations
ELASTICSEARCH_URL = "localhost:9200"
ES_USERNAME = "test"
ES_PASSWORD = "test"

# logging.info(f"current elasticsearch host:{ELASTICSEARCH_URL};es_user:{ES_USERNAME};es_password:{ES_PASSWORD}")


# mysql configurations
MYSQL_HOST = "127.0.0.1:3306"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "alwin"
MYSQL_DB = "digital_labor"


# logging.info(f"current mysql host:{MYSQL_HOST};mysql_user:{MYSQL_USERNAME};mysql_password:{MYSQL_PASSWORD}")


SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
)


# other configurations
# llm服务信息

API_FOR_OPEN_LLM_WS_URL = "http://localhost:11434/v1/chat/completions"

API_FOR_QWEN2HALF_32B_URL_PREFIX = "http://localhost:11434/v1"

MODEL_NAME_QWEN2HALF_32B = "qwen2.5:32b-instruct"

API_FOR_QWEN2HALF_7B_URL_PREFIX = "http://localhost:11434/v1"

MODEL_NAME_QWEN2HALF_7B = "qwen2.5:7b-instruct"

# triton服务信息
TRITON_INFERENCE_SERVER_GRPC_URL = "localhost"

# 默认表名
# es表名

DEFAULT_ELASTICSEARCH_KB_NAME = "digital_labor"

# milvus表名
DEFAULT_MILVUS_KB_NAME = "digital_labor"

DEFAULT_MILVUS_CHUNK_DB_NAME = "digital_labor_chunk"

# logging.info(f"默认es表名{DEFAULT_ELASTICSEARCH_KB_NAME}，默认milvus表名{DEFAULT_MILVUS_KB_NAME},{DEFAULT_MILVUS_CHUNK_DB_NAME}")



# logger.info("environment: {}".format(environment))

# langfuse配置
LANGFUSE_SK = "sk-lf-5fb543e1-2215-453b-9707-c003a26eb82c"
LANGFUSE_PK = "pk-lf-37bf86ac-f2f4-45de-a8ea-534dd62a5b4f"
LANGFUSE_HOST = "http://localhost:3001"

logger.info(f"current project langfuse settings:host:{LANGFUSE_HOST}, secret_key:{LANGFUSE_SK}, public_key:{LANGFUSE_PK}")

# ocr sit url
OCR_URL = "localhost"
