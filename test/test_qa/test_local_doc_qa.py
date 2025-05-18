import os
import sys

sys.path.append("././")

from chains.local_rag import LocalRAG
from chains.local_chunk_rag import LocalChunkRAG
from chains.local_hybrid_rag import LocalHybridRag

from utils.traceback import langfuse,langfuse_handler
from utils.llm_util import post_api_for_llm,post_api_for_llm_batch
from db.service.milvus_chunk_db_service import default_chunk_db
from configs.model_config import CRAG_PROMPT_NAME,HYDE_PROMPT_NAME,MODEL_NAME_QWEN2HALF_32B

local_hybrid_rag = LocalHybridRag()

if __name__ == "__main__":
    query="申报这个职称，需要满足什么条件？"
    history = [
        {
            "role": "user",
            "content": "工程系列职称，哪些专业可以申报"
        },
        {
            "role": "assistant",
            "content": """根据《中国航空工业集团有限公司工程系列职称评审细则》中的规定，工程系列职称可以申报的专业包括但不限于以下几类：

1. 体系技术专业
2. 飞行器技术专业
3. 航电技术专业
4. 机电技术专业
5. 飞行控制技术专业
6. 武器技术专业
7. 动力技术专业
8. 航空制造技术专业
9. 航空材料技术专业
10. 试验与试飞技术专业
11. 基础与共性技术专业
12. 前沿技术专业
13. 技术管理专业
14. 其他工程技术专业

这些专业适用于从事相关专业的研究、设计、制造、工艺、试验、验证、定型/鉴定/符合性验证、测试、技术开发、维护、修理等领域的工程技术人员。具体申报条件和要求请参照细则中的相关规定。
            """
        },
        {
            "role": "user",
            "content": "飞行器技术专业包括哪些？"
        },
        {
            "role": "assistant",
            "content": """根据提供的文件内容，飞行器技术专业包括以下具体专业：

- 飞行器总体
- 空气动力（含水动力、载荷）
- 进排气系统
- 结构（含热结构、热防护）
- 强度（含静、动、疲劳强度，振动与噪声）
- 旋翼系统
- 隐身
- 高超声速飞行器专用技术
- 特种飞机专用技术
- 无人机系统

这些专业涵盖了飞行器技术领域的多个方面。
"""
        }
    ]

    query="门店灯片坏了怎么换？"
    history = [
        {
            "role": "user",
            "content": "门店灯片坏了怎么换？"
        },
        {
            "role": "assistant",
            "content": """如果门店的灯片损坏，需要登录屈购系统进行订购。具体步骤如下：
检查店铺的陈列工具（如灯箱/灯片/托盘/层板等）是否异常。
核对陈列物料内容，确认是否为最新陈列图要求。
如果发现灯片破损或缺失，则登录屈购系统进行订购。
确保灯片尺寸正确，如果店铺物料尺寸更新升级，请通过邮件或钉钉联系相关市场负责人修改信息，以确保收到正确版本的物料。"""
        },
        {
            "role": "user",
            "content": "门店灯片坏了"
        },
        {
            "role": "assistant",
            "content": """如果门店的灯片损坏，需要登录屈购系统进行订购。具体步骤如下：
检查店铺的陈列工具（如灯箱/灯片/托盘/层板等）是否异常。
核对陈列物料内容，确认是否为最新陈列图要求。
如果发现灯片破损或缺失，则登录屈购系统进行订购。
确保灯片尺寸正确，如果店铺物料尺寸更新升级，请通过邮件或钉钉联系相关市场负责人修改信息，以确保收到正确版本的物料。"""
        }
    ]

    query = "门店灯片坏了"
    history = [
        {
            "role": "user",
            "content": "门店灯片坏了怎么换？"
        },
        {
            "role": "assistant",
            "content": """这个问题暂时未覆盖，数字员工还在学习升级"""
        }
    ]

    query = "店铺没人了，我有急事外出怎么办？"
    def hyde(query):
        # template="""Given a question, generate a paragraph of text that answers the question.
        #         Question: {question}
        #         Paragraph:"""

        # answer = post_api_for_llm(template.format(question=query))

        prompt = langfuse.get_prompt(HYDE_PROMPT_NAME).compile(question=query)
        answer = post_api_for_llm(prompt,model_name=MODEL_NAME_QWEN2HALF_32B)

        related_chunks = default_chunk_db.do_search(
            query=answer,
            score_threshold=0.3
        )
        # print(related_chunks)

        prompts = [langfuse.get_prompt(CRAG_PROMPT_NAME).compile(
                            context=related_chunk['raw_text'], question=query
                        ) for related_chunk in related_chunks ]
        related_chunk_grade_scores = post_api_for_llm_batch(prompts=prompts,model_name=MODEL_NAME_QWEN2HALF_32B)
        print(related_chunk_grade_scores)

    query = "灯片坏了怎么换？"
    query = "店铺没人了，我有急事外出怎么办？"


    hyde(query)

    # history = []
    # import uuid
    # trace_id = "xnihnswfei"
    # user_id = "157000"
    # session_id = None
    # if not session_id:
    #     session_id = str(uuid.uuid4())

    # for resp,history in local_hybrid_rag.dialog_onetune(query,
    #                                                     chat_history=history,
    #                                                     trace_id=trace_id,
    #                                                     user_id=user_id,
    #                                                     session_id=session_id
    #                                                     ):
    #     print(resp)
 
    
