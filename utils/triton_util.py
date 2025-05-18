# coding: utf-8
import os
import sys
import time
import logging
from typing import Dict, List

import numpy as np
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException

sys.path.append("./")
from configs.model_config import (
    embed_model_triton_service_dict,
    EMBEDDING_MODEL,
    RERANK_MODEL,
)
from configs.apollo_config import TRITON_INFERENCE_SERVER_GRPC_URL


def embedding_func(
    texts: List[str],
    model_name: str = EMBEDDING_MODEL,
    batch_size: int = 4,
    output_name="logits",
):
    res = []
    triton_client = grpcclient.InferenceServerClient(
        url=TRITON_INFERENCE_SERVER_GRPC_URL,
        verbose=False,
        ssl=False,
        root_certificates=None,
        private_key=None,
        certificate_chain=None,
        channel_args=[("grpc.enable_retries", True)],
    )
    total_nums = len(texts)

    model_name = embed_model_triton_service_dict.get(model_name)
    if isinstance(model_name, dict):
        output_name = model_name.get("output_name")
        model_name = model_name.get("model_name")

    def infer_batch(texts, model_name=model_name):
        """控制triton显存使用量"""
        batch_size = len(texts)
        inputs = []
        inputs.append(grpcclient.InferInput("TEXT", [batch_size], "BYTES"))
        in0n = np.array([x.encode("utf-8") for x in texts])
        inputs[0].set_data_from_numpy(in0n)
        outputs = []
        outputs.append(grpcclient.InferRequestedOutput(output_name))
        results = triton_client.infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs,
            compression_algorithm=None,
        )
        res = results.as_numpy(output_name)
        return res

    total_batchs = (
        (total_nums // batch_size)
        if total_nums % batch_size == 0
        else (total_nums // batch_size + 1)
    )

    for i in range(total_batchs):
        batch_texts = texts[i * batch_size : (i + 1) * batch_size]
        batch_vectors = infer_batch(batch_texts)
        if i == 0:
            res = batch_vectors
        else:
            res = np.append(res, batch_vectors, axis=0)
    return res


def rerank_func(
    texts: List[List[str]], model_name: str = RERANK_MODEL, batch_size: int = 4
):
    """
    rerenk重排序方法，输入是问答pairs
    texts: List[List[str]]: 2D list of text, each sublist contains two text for reranking

    return: List[float]: 1D list of rerank scores
    """
    res = []
    triton_client = grpcclient.InferenceServerClient(
        url=TRITON_INFERENCE_SERVER_GRPC_URL,
        verbose=False,
        ssl=False,
        root_certificates=None,
        private_key=None,
        certificate_chain=None,
        channel_args=[("grpc.enable_retries", True)],
    )
    total_nums = len(texts)

    model_name = embed_model_triton_service_dict.get(model_name)
    print(model_name)

    def infer_batch(texts, model_name=model_name):
        """控制triton显存使用量"""
        batch_size = len(texts)
        inputs = []
        inputs.append(grpcclient.InferInput("TEXT", [batch_size, 2], "BYTES"))
        in0n = np.array([[x.encode("utf-8") for x in d] for d in texts])
        inputs[0].set_data_from_numpy(in0n)
        outputs = []
        outputs.append(grpcclient.InferRequestedOutput("logits"))

        results = triton_client.infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs,
            compression_algorithm=None,
        )
        res = results.as_numpy("logits")
        return res.flatten()

    total_batchs = (
        (total_nums // batch_size)
        if total_nums % batch_size == 0
        else (total_nums // batch_size + 1)
    )

    for i in range(total_batchs):
        batch_texts = texts[i * batch_size : (i + 1) * batch_size]
        batch_vectors = infer_batch(batch_texts)
        if i == 0:
            res = batch_vectors
        else:
            res = np.append(res, batch_vectors, axis=0)
    return res


if __name__ == "__main__":

    # test embedding_func
    # texts = [
    #     "今天行星期几",
    #     "你好啊",
    #     "你是谁",
    #     "我是谁",
    #     "今天出门",
    #     "今天天气不错",
    #     "今天天气不错呀",
    # ]

    # texts = ["你是谁"]

    # texts = ["天虹的请假流程是什么"]

    texts = [
        """片段总结:公司实行打卡制度，规范包括禁止代打卡、忘打卡需备案，以及对迟到、早退、旷工的处罚规定，各类休假需通过HR系统申请，特别规定了病假、事假、工伤假的申请流程和材料要求，其中病假需提供真实材料，工伤假需劳动能力鉴定，超过规定假期未归按旷工处理。\n\n文档总结:本文档是：9.6.1.1考勤管理制度，内容是关于：公司员工的考勤管理规定，包括工作时间、加班、打卡规范、各类休假申请流程及规定，以及医疗期的说明。\n\n3.4打卡规范员工实行打卡制度。不得托人打卡或代人打卡,忘打卡需当天在部门考勤员处备案;每月忘打卡达到三次及以上、托人打卡或代人打卡的,处理办法详见《员工奖惩管理规范》。\n3.5旷工员工未经审批缺岗4小时及以上即认定为旷工。旷工处理办法详见《员工奖惩管理规范》。\n3.6迟到早退擅离岗位员工未按时上下班即为迟到或早退或擅离岗位。迟到早退擅离岗位处理办法详见《员工奖惩管理规范》。\n3.7休假各类假别均需在公司HR系统“员工自助—我要请假”中提交申请。休假申请需在休假前完成提交审批,如因事情紧急无法提前办理请假手续,可由员工本人或家属在24小时内以短信、微信等形式通知直接上级办理请假手续,并于假期结束上班后,补办请假手续。\n3.7.1病假病假是指员工本人因生病或非因工负伤,根据医生提供的休假建议给予批准的休假时间。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/BO0sPGX0uoC3BMVkvoGSlkD7.png)病假审批材料:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/nQo5VwlIFhDvYaLclQeTAb9F.png)注:(1)所有病假材料交内勤验原件,收复印件。如员工提供虚假病假材料,本次请假将按严重违反公司纪律进行处罚,视为旷工;(2)公司需要核实病情及病假情况时,员工应配合,公司如对员工就诊医院诊断证明持有异议,可另行指定医院复查或前往市镇级以上劳动能力鉴定委员会进行鉴定,员工无正当理由拒绝,本次请假视为旷工;(3)试用期员工病休假超过5天(含5天),试用期中止,试用期员工返岗后试用期可相应延长。\n3.7.2事假公司根据现场经营需要有权利不批准事假,员工请事假,必须提前一天说明,当天/事后请假者原则上不予以批准,未经批准擅自休假或超假者,一律按旷工处理;连续请事假时间原则上不可超过一个月。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/wklJtRhqQpEAdQMZ5PmexFRI.png)\n3.7.3工伤假工伤假是指员工因工负伤,且被劳动能力鉴定部门认定为工伤的,劳动能力鉴定委员会认定需要暂停工作进行治疗期间,一般不超过12个月。\n3.7.3.1工伤的定义员工有下列情形之一的,公司应向社保部门为其申请工伤:在工作时间和工作场所内,因工作原因受到事故伤害的;(2)工作时间前后在工作场所内,从事与工作有关的预备性或收尾性工作受到事故伤害的;(3)在工作时间和工作场所内,因履行工作职责受到暴力等意外伤害的;(4)因工外出期间,由于工作原因受到伤害或者发生事故下落不明的;(5)在上下班途中,受到非本人主要责任的交通事故或者城市轨道交通、客运轮渡、火车事故伤害的;(6)在工作时间和工作岗位,突发疾病死亡或者在四十八小时之内经抢救无效死亡的;(7)在抢险救灾等维护国家利益、公共利益活动中受到伤害的;(8)法律、规定应当认定为工伤的其他情形。\n3.7.3.2工伤假的核定(1)伤害的程度、伤害的部位;(2)就诊医院出具的有关治疗和休息以及门诊治疗时间的建议;(3)实际住院治疗的时间;(4)工伤员工所在工作岗位以及工作内容的性质;(5)工伤员工所在部门主管的意见;(6)工伤员工本人的意见;(7)对工伤员工的治疗和工作有影响的其他因素;(8)工伤假期的期限不少于住院的期限,但可以根据具体情况少于医生建议休息的期限;(9)员工发生工伤申请工伤假期时,应当以所就医医院核定及劳动能力鉴定委员会认定的假期为准;(10)医院应该根据工伤员工是否需要住院分别核定其工伤假期。如果不需要住院的,由医院予以核定;如果需要住院的,其工伤假期一般包括住院期间以及出院后休息和治疗期间。其中出院后的休息和治疗期间可参考医院根据就诊医院的建议和员工伤害程度以及伤害部位并结合其工作内容等因素合理确定,最终期限以劳动能力鉴定委员会认定意见为准;(11)员工本人要求进行“劳动能力等级鉴定”的,可以申请“劳动能力等级鉴定”;有伤残、骨折情形的,必须进行“劳动能力等级鉴定”,工伤假期的期限则以劳动保障部门申请核定工伤假期为准;(12)员工在核定的工伤假期内其薪资继续发放,核定的工伤假期结束后,员工应当及时回公司上班,如因伤势影响其从事原工作的,可由所在部门主管合理安排其他工作/岗位,其薪资按新岗位/工作确定,上班期间如仍需要门诊治疗的,医院和所在部门应当予以适当照顾,保证其在上班期间不影响治疗;(13)工伤员工超过核定的工伤假期不回公司上班的,应当根据公司要求申请病假或事假,否则以旷工论处;(14)员工发生工伤,其本人、家属或者所在部门应当在48小时内以邮件形式通知所属城市社保负责人,社保负责人根据社保工伤要求及员工提交材料初步审核批准后,可先暂按工伤假处理,即可按照上述规定享受一定的工伤假期和其他工伤待遇。如最终经社保局工伤认定部门未认定为工伤的,则之前申请的工伤假需按病假或事假处理,公司多发工伤相关待遇将从员工薪资待遇中予以扣回。审批流程:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/xD5YoKwdPh40LknNxAOvmSVU.png)工伤假审批材料:![](https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/13/Qv4C2q8TdLJqkWfDMtIjomlj.png)\n"""
    ]
    res = embedding_func(texts, model_name="bge-m3")
    print(res.shape, type(res[0]))
    # print(res)

    # test rerank_func
    # texts = [['what is panda?', 'hi'],
    #          ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
    # res = rerank_func(texts)
    # print(res)
