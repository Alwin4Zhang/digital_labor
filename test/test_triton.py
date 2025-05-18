# coding: utf-8
import sys

sys.path.append("./")
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException


# triton_client = grpcclient.InferenceServerClient(
#     url="192.168.148.148:8010"
# )

# if not triton_client.is_server_live(headers={"test": "1", "dummy": "2"}):
#     print("FAILED : is_server_live")

# if not triton_client.is_server_ready():
#     print("FAILED : is_server_ready")

# # print(triton_client.get_server_metadata())

# # metadata = triton_client.get_model_metadata(
# #     "bge_feature_ensemble", headers={"test": "1", "dummy": "2"}
# # )


# config = triton_client.get_model_config(
#     "bge_feature_ensemble"
# )

# print(config.config.name)

from db.embedding_utils import embed_texts_api

import numpy as np

texts = [
    "手机如何下载安装并使用aTrust安全软件",
    "电脑如何下载安装并使用aTrust安全软件",
    "平板如何下载安装并使用aTrust安全软件"
]

embs = embed_texts_api(texts,return_numpy=True)

print(len(embs))

# t = np.array(embs) @ np.array(embs).T
# t = np.tril(t,-1)
# print(t,np.where(t > 0.85))

text2 = ["你是谁"]

embs2 = embed_texts_api(text2,return_numpy=True)

t = embs2 @ embs.T

print(np.where( t> 0.1))

from db.service.milvus_chunk_db_service import default_chunk_db

# res = client.search(
#     collection_name="quick_setup", # Replace with the actual name of your collection
#     data=[
#         [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104],
#         [0.3172005263489739, 0.9719044792798428, -0.36981146090600725, -0.4860894583077995, 0.95791889146345]
#     ], # Replace with your query vectors
#     limit=2, # Max. number of search results to return
#     search_params={"metric_type": "IP", "params": {}} # Search parameters
# )

# result = json.dumps(res, indent=4)
# print(result)


# TODO:查询ids对应的文档
ids = [
    "457343369696522437",
    "457343369696522438",
    "457343369696522439",
    "457343369696522440"
]

# docs = default_chunk_db.milvus.query(
#     "digital_labor_chunk_avic",
#     filter=f"id in {ids}"
# )

# res = default_chunk_db.milvus.get(
#     collection_name="digital_labor_chunk_avic",
#     ids=ids,
#     output_fields=["vector", "color"]
# )


# config = triton_client.get_model_config(
#     "bge_feature_ensemble"
# )

# print(config.config.name)
# print(len(res))
