# coding: utf-8
import sys

sys.path.append("./")

import os
import logging
from typing import Dict, List

import numpy as np
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings

from utils.triton_util import embedding_func, rerank_func

from configs.model_config import (
    embedding_model_dict,
    EMBEDDING_MODEL,
    EMBEDDING_DEVICE,
    RERANK_MODEL,
    use_local,
)

from configs.apollo_config import logger

embed_model = None

def normalize(embedding: np.ndarray, p=2, dim=1, eps=1e-12) -> np.ndarray:
    """'标准化向量"""
    norms = np.linalg.norm(embedding, ord=p, axis=dim, keepdims=True)
    norms = np.clip(norms, a_min=eps, a_max=None)
    output = embedding / norms
    return output

def load_local_embeddings(
    model_name: str = None, device: str = EMBEDDING_DEVICE, norm: bool = False
) -> Embeddings:
    model_name = model_name if model_name else EMBEDDING_MODEL
    model_name_or_path = (
        embedding_model_dict.get(model_name)
        if embedding_model_dict.get(model_name)
        else embedding_model_dict.get(EMBEDDING_MODEL)
    )
    encode_kwargs = {"normalize_embeddings": norm}
    if "bge-" in model_name:
        HFEmbs = HuggingFaceBgeEmbeddings
    else:
        HFEmbs = HuggingFaceEmbeddings
    embeddings = HFEmbs(
        model_name=model_name_or_path,
        model_kwargs={"device": device},
        encode_kwargs=encode_kwargs,
    )
    return embeddings


if use_local:
    embed_model = load_local_embeddings(
        model_name=EMBEDDING_MODEL, device=EMBEDDING_DEVICE, norm=True
    )


def embed_texts(texts: List[str], embed_model: Embeddings = embed_model):
    """将文本向量化"""
    embeddings = None
    try:
        embeddings = embed_model.embed_documents(texts)
    except Exception as e:
        logger.error(e)
    return embeddings


def embed_documents(
    docs: List[Document], embed_model: Embeddings = embed_model
) -> Dict:
    """将Langchain-Document向量化"""
    texts = [x.page_content for x in docs]
    metadatas = [x.metadata for x in docs]
    embeddings = embed_texts(texts=texts, embed_model=embed_model)
    if not embeddings:
        return {}
    return {"texts": texts, "embeddings": embeddings, "metadatas": metadatas}


def embed_texts_api(
    texts: List[str], model_name: str = EMBEDDING_MODEL, norm=True, return_numpy=False
):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = embedding_func(texts, model_name=model_name)
    if norm:
        embeddings = normalize(embeddings)
    if return_numpy:
        return embeddings
    return embeddings.tolist()


def embed_documents_api(
    docs: List[Document], model_name: str = EMBEDDING_MODEL, norm=True
) -> Dict:
    """将Langchain-Document向量化"""
    texts = [x.page_content for x in docs]
    metadatas = [x.metadata for x in docs]
    embeddings = embed_texts_api(texts=texts, model_name=model_name, norm=norm)
    if not embeddings:
        return {}
    return {"texts": texts, "embeddings": embeddings, "metadatas": metadatas}


def rerank_texts_api(
    query: str, candidates: List[str], model_name: str = RERANK_MODEL, verbose=False
):
    """chunks召回后的重排，返回rerank后的结果"""
    texts = [[query, candidate] for candidate in candidates]
    scores = rerank_func(texts, model_name=model_name)
    sorted_idx = np.argsort(scores)[::-1]
    if verbose:
        return [(i, texts[i][-1], scores[i]) for i in sorted_idx]
    return [texts[i][-1] for i in sorted_idx]


if __name__ == "__main__":
    # texts = ["你好，世界！", "你好，世界！", "你好，世界！"]
    # embeddings = embed_texts_api(texts)
    # print(embeddings)

    import numpy as np

    texts = [
        "湖南地区育儿假、独生子女父母护理假执行方案根据2021年12月3日湖南省第十三届人民代表大会常务委员会第二十七次会议通过的《湖南省人口与计划生育条例》中关于新增育儿假、独生子女父母护理假的内容,基于新增假别,湖南地区新增育儿假、独生子女父母护理假执行方案如下:",
        """一、育儿假1.育儿假的定义:符合法定生育条件的夫妻,在子女3周岁以内,夫妻双方每年均可享受10天育儿假。2.假期安排:《条例》发布之日(2021年12月3日)起,符合政策规定生育子女的夫妻,子女在3周岁之前,公司给予夫妻双方每年分别享受10天的育儿假。国家法定休假日不计入育儿假假期。每年的育儿假不按照子女数量叠加享受。注:(1)当年度新入职、离职员工可享受的假期天数,应当按照员工当年已工作时间折算应休未休育儿假天数。折算方法为:(当年度在本单位已过日历天数÷365天)×员工当年度应享受的育儿假天数-当年度已安排育儿假天数。折算后不满一天时,舍零取整。如出现员工多休育儿假情况,按事假扣回。(2)如员工的育儿假在《条例》发布之日至公司政策还未公布期间的,可以按照《条例》规定享受应得育儿假。员工的育儿假可以一次性享受,也可以分次享受。当年度未休完的育儿假作清零处理,不另行计发加班工资,也不可延长下一年度补休。3.需提供资料:持生育证明、子女的户口本、子女的出生医学证明等资料到所在部门申请,流程通过后方可享受育儿假。4.其他:若员工所在地关于育儿假另有政策规定的,以当地政策为准。""",
        "二、独生子女父母护理假1.独生子女父母护理假的定义:父母年满60周岁,因病住院治疗期间,其独生子女每年可累计享受15天的护理假。2.假期安排:《条例》发布之日(2021年12月3日)起,符合政策法规的独生子女员工,其父母年满60周岁后患病住院期间,独生子女员工每年享受15天的护理假,其每年享受的父母护理假可以一次性享受,也可以分次享受。3.需提供的资料:持独生子女父母光荣证或独生子女证、父母身份证件、医疗机构诊断证明、住院证明(住院病案首页、入院记录、出院记录)等资料到所在部门申请,流程通过后方可享受独生子女父母护理假。注:(1)当年度新入职、离职员工可享受的假期天数,应当按照员工当年已工作时间折算应休未休护理假天数。折算方法为:(当年度在本单位已过日历天数÷365天)×员工当年度应享受的护理假天数-当年度已安排护理假天数。折算后不满一天时,舍零取整。如出现员工多休护理假情况,按事假扣回。(2)当年度未休完的护理假作清零处理,不另行计发加班工资,也不可延长至下一年度补休。(3)申请时无法提供住院证明相关材料的,需在假期结束之日起七个工作日内及时提交,由内勤核验原件,留存复印件归档。逾期不交者,将按照弄虚作假处理。4.其他:若员工所在地关于独生子女父母护理假另有政策规定的,以当地政策为准。审批流程:审批材料:",
        "三、关于休假的其他说明(1)适用对象:湖南地区购物中心、百货、超市事业部、物流中心全体全职自营员工;(2)若员工所在地关于育儿假、独生子女父母护理假另有政策规定的,以当地政策为准;(3)本方案未尽事项,由湖南区行政管理部结合湖南省相关政策文件规定另行处理。",
        "四、湖南省关于育儿假、独生子女父母护理假相关政策文件如下:",
        "(1)湖南省人口与计划生育条例;为何新增两个假期——新修订的湖南人口计生条例解读。",
        "湖南区行政管理部",
    ]

    embs = embed_texts_api(texts)

    print(len(embs))

    print(np.array(embs) @ np.array(embs).T)

    # texts = ["""片段总结:公司实行打卡制度，规范包括禁止代打卡、忘打卡需备案，以及对迟到、早退、旷工的处罚规定，各类休假需通过HR系统申请，特别规定了病假、事假、工伤假的申请流程和材料要求，其中病假需提供真实材料，工伤假需劳动能力鉴定，超过规定假期未归按旷工处理。\n\n文档总结:本文档是：9.6.1.1考勤管理制度，内容是关于：公司员工的考勤管理规定，包括工作时间、加班、打卡规范、各类休假申请流程及规定，以及医疗期的说明。\n\n3.4打卡规范员工实行打卡制度。不得托人打卡或代人打卡,忘打卡需当天在部门考勤员处备案;每月忘打卡达到三次及以上、托人打卡或代人打卡的,处理办法详见《员工奖惩管理规范》。\n3.5旷工员工未经审批缺岗4小时及以上即认定为旷工。旷工处理办法详见《员工奖惩管理规范》。\n3.6迟到早退擅离岗位员工未按时上下班即为迟到或早退或擅离岗位。迟到早退擅离岗位处理办法详见《员工奖惩管理规范》。\n3.7休假各类假别均需在公司HR系统“员工自助—我要请假”中提交申请。休假申请需在休假前完成提交审批,如因事情紧急无法提前办理请假手续,可由员工本人或家属在24小时内以短信、微信等形式通知直接上级办理请假手续,并于假期结束上班后,补办请假手续。\n3.7.1病假病假是指员工本人因生病或非因工负伤,根据医生提供的休假建议给予批准的休假时间。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/BO0sPGX0uoC3BMVkvoGSlkD7.png)病假审批材料:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/nQo5VwlIFhDvYaLclQeTAb9F.png)注:(1)所有病假材料交内勤验原件,收复印件。如员工提供虚假病假材料,本次请假将按严重违反公司纪律进行处罚,视为旷工;(2)公司需要核实病情及病假情况时,员工应配合,公司如对员工就诊医院诊断证明持有异议,可另行指定医院复查或前往市镇级以上劳动能力鉴定委员会进行鉴定,员工无正当理由拒绝,本次请假视为旷工;(3)试用期员工病休假超过5天(含5天),试用期中止,试用期员工返岗后试用期可相应延长。\n3.7.2事假公司根据现场经营需要有权利不批准事假,员工请事假,必须提前一天说明,当天/事后请假者原则上不予以批准,未经批准擅自休假或超假者,一律按旷工处理;连续请事假时间原则上不可超过一个月。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/wklJtRhqQpEAdQMZ5PmexFRI.png)\n3.7.3工伤假工伤假是指员工因工负伤,且被劳动能力鉴定部门认定为工伤的,劳动能力鉴定委员会认定需要暂停工作进行治疗期间,一般不超过12个月。\n3.7.3.1工伤的定义员工有下列情形之一的,公司应向社保部门为其申请工伤:在工作时间和工作场所内,因工作原因受到事故伤害的;(2)工作时间前后在工作场所内,从事与工作有关的预备性或收尾性工作受到事故伤害的;(3)在工作时间和工作场所内,因履行工作职责受到暴力等意外伤害的;(4)因工外出期间,由于工作原因受到伤害或者发生事故下落不明的;(5)在上下班途中,受到非本人主要责任的交通事故或者城市轨道交通、客运轮渡、火车事故伤害的;(6)在工作时间和工作岗位,突发疾病死亡或者在四十八小时之内经抢救无效死亡的;(7)在抢险救灾等维护国家利益、公共利益活动中受到伤害的;(8)法律、规定应当认定为工伤的其他情形。\n3.7.3.2工伤假的核定(1)伤害的程度、伤害的部位;(2)就诊医院出具的有关治疗和休息以及门诊治疗时间的建议;(3)实际住院治疗的时间;(4)工伤员工所在工作岗位以及工作内容的性质;(5)工伤员工所在部门主管的意见;(6)工伤员工本人的意见;(7)对工伤员工的治疗和工作有影响的其他因素;(8)工伤假期的期限不少于住院的期限,但可以根据具体情况少于医生建议休息的期限;(9)员工发生工伤申请工伤假期时,应当以所就医医院核定及劳动能力鉴定委员会认定的假期为准;(10)医院应该根据工伤员工是否需要住院分别核定其工伤假期。如果不需要住院的,由医院予以核定;如果需要住院的,其工伤假期一般包括住院期间以及出院后休息和治疗期间。其中出院后的休息和治疗期间可参考医院根据就诊医院的建议和员工伤害程度以及伤害部位并结合其工作内容等因素合理确定,最终期限以劳动能力鉴定委员会认定意见为准;(11)员工本人要求进行“劳动能力等级鉴定”的,可以申请“劳动能力等级鉴定”;有伤残、骨折情形的,必须进行“劳动能力等级鉴定”,工伤假期的期限则以劳动保障部门申请核定工伤假期为准;(12)员工在核定的工伤假期内其薪资继续发放,核定的工伤假期结束后,员工应当及时回公司上班,如因伤势影响其从事原工作的,可由所在部门主管合理安排其他工作/岗位,其薪资按新岗位/工作确定,上班期间如仍需要门诊治疗的,医院和所在部门应当予以适当照顾,保证其在上班期间不影响治疗;(13)工伤员工超过核定的工伤假期不回公司上班的,应当根据公司要求申请病假或事假,否则以旷工论处;(14)员工发生工伤,其本人、家属或者所在部门应当在48小时内以邮件形式通知所属城市社保负责人,社保负责人根据社保工伤要求及员工提交材料初步审核批准后,可先暂按工伤假处理,即可按照上述规定享受一定的工伤假期和其他工伤待遇。如最终经社保局工伤认定部门未认定为工伤的,则之前申请的工伤假需按病假或事假处理,公司多发工伤相关待遇将从员工薪资待遇中予以扣回。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/xD5YoKwdPh40LknNxAOvmSVU.png)工伤假审批材料:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/Qv4C2q8TdLJqkWfDMtIjomlj.png)\n"""]
    # texts = ["test"]
    # res = embed_texts_api(texts)
    # # print(res.shape, type(res[0]))
    # print(res)

    # texts = [
    #     ['what is panda?', 'hi'],
    #     ['what is panda?', "I don't know"],
    #     ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.'],
    # ]

    # res = rerank_texts_api(texts,verbose=True)
    # print(res)
