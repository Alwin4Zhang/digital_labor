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
    "湖南地区育儿假、独生子女父母护理假执行方案根据2021年12月3日湖南省第十三届人民代表大会常务委员会第二十七次会议通过的《湖南省人口与计划生育条例》中关于新增育儿假、独生子女父母护理假的内容,基于新增假别,湖南地区新增育儿假、独生子女父母护理假执行方案如下:",
    """一、育儿假1.育儿假的定义:符合法定生育条件的夫妻,在子女3周岁以内,夫妻双方每年均可享受10天育儿假。2.假期安排:《条例》发布之日(2021年12月3日)起,符合政策规定生育子女的夫妻,子女在3周岁之前,公司给予夫妻双方每年分别享受10天的育儿假。国家法定休假日不计入育儿假假期。每年的育儿假不按照子女数量叠加享受。注:(1)当年度新入职、离职员工可享受的假期天数,应当按照员工当年已工作时间折算应休未休育儿假天数。折算方法为:(当年度在本单位已过日历天数÷365天)×员工当年度应享受的育儿假天数-当年度已安排育儿假天数。折算后不满一天时,舍零取整。如出现员工多休育儿假情况,按事假扣回。(2)如员工的育儿假在《条例》发布之日至公司政策还未公布期间的,可以按照《条例》规定享受应得育儿假。员工的育儿假可以一次性享受,也可以分次享受。当年度未休完的育儿假作清零处理,不另行计发加班工资,也不可延长下一年度补休。3.需提供资料:持生育证明、子女的户口本、子女的出生医学证明等资料到所在部门申请,流程通过后方可享受育儿假。4.其他:若员工所在地关于育儿假另有政策规定的,以当地政策为准。""",
    "二、独生子女父母护理假1.独生子女父母护理假的定义:父母年满60周岁,因病住院治疗期间,其独生子女每年可累计享受15天的护理假。2.假期安排:《条例》发布之日(2021年12月3日)起,符合政策法规的独生子女员工,其父母年满60周岁后患病住院期间,独生子女员工每年享受15天的护理假,其每年享受的父母护理假可以一次性享受,也可以分次享受。3.需提供的资料:持独生子女父母光荣证或独生子女证、父母身份证件、医疗机构诊断证明、住院证明(住院病案首页、入院记录、出院记录)等资料到所在部门申请,流程通过后方可享受独生子女父母护理假。注:(1)当年度新入职、离职员工可享受的假期天数,应当按照员工当年已工作时间折算应休未休护理假天数。折算方法为:(当年度在本单位已过日历天数÷365天)×员工当年度应享受的护理假天数-当年度已安排护理假天数。折算后不满一天时,舍零取整。如出现员工多休护理假情况,按事假扣回。(2)当年度未休完的护理假作清零处理,不另行计发加班工资,也不可延长至下一年度补休。(3)申请时无法提供住院证明相关材料的,需在假期结束之日起七个工作日内及时提交,由内勤核验原件,留存复印件归档。逾期不交者,将按照弄虚作假处理。4.其他:若员工所在地关于独生子女父母护理假另有政策规定的,以当地政策为准。审批流程:审批材料:",
    "三、关于休假的其他说明(1)适用对象:湖南地区购物中心、百货、超市事业部、物流中心全体全职自营员工;(2)若员工所在地关于育儿假、独生子女父母护理假另有政策规定的,以当地政策为准;(3)本方案未尽事项,由湖南区行政管理部结合湖南省相关政策文件规定另行处理。",
    "四、湖南省关于育儿假、独生子女父母护理假相关政策文件如下:",
    "(1)湖南省人口与计划生育条例;为何新增两个假期——新修订的湖南人口计生条例解读。",
    "湖南区行政管理部"
]

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
