import os
import sys

sys.path.append("./")

import uuid
import json
import asyncio
import requests
from typing import Tuple
import tiktoken
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from utils.common import timeit
from utils.traceback import langfuse,langfuse_handler

# from websockets.sync.client import connect
# from websocket import create_connection

from configs.apollo_config import (
    API_FOR_QWEN2HALF_32B_URL_PREFIX,
    API_FOR_QWEN2HALF_7B_URL_PREFIX,
    MODEL_NAME_QWEN2HALF_32B,
    MODEL_NAME_QWEN2HALF_7B ,
)

from typing import Tuple
import tiktoken


# 手动下载tiktoken，离线使用
tiktoken_cache_dir = os.path.dirname(os.path.dirname(__file__))
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir
# validate
assert os.path.exists(os.path.join(tiktoken_cache_dir,"9b5ad71b2ce5302211f9c61530b329a4922fc6a4"))

class ChatOpenAIIn05(ChatOpenAI):
    def _get_encoding_model(self) -> Tuple[str, tiktoken.Encoding]:
        """
        Override the method to return a hardcoded valid model and its encoding.
        """
        # Set the model to a valid one to avoid errors
        model = "gpt-3.5-turbo"
        return model, tiktoken.encoding_for_model(model)


llm_qwen2half_32b = ChatOpenAIIn05(
    model=MODEL_NAME_QWEN2HALF_32B,
    openai_api_key="EMPTY",
    openai_api_base=API_FOR_QWEN2HALF_32B_URL_PREFIX,
    temperature=0,
    frequency_penalty=1.2,
    max_tokens=1024
)

llm_qwen2half_7b = ChatOpenAIIn05(
    model=MODEL_NAME_QWEN2HALF_7B ,
    openai_api_key="EMPTY",
    openai_api_base=API_FOR_QWEN2HALF_7B_URL_PREFIX,
    temperature=0,
    frequency_penalty=1.2,
    max_tokens=1024
)

llm_qwen2half_7b_stream = ChatOpenAIIn05(
    model=MODEL_NAME_QWEN2HALF_7B ,
    openai_api_key="EMPTY",
    openai_api_base=API_FOR_QWEN2HALF_7B_URL_PREFIX,
    temperature=0,
    default_headers={
        "x-gateway-accept": "text/event-stream"
    }
)

llm_qwen2half_32b_stream = ChatOpenAIIn05(
    model=MODEL_NAME_QWEN2HALF_32B,
    openai_api_key="EMPTY",
    openai_api_base=API_FOR_QWEN2HALF_32B_URL_PREFIX,
    temperature=0,
    default_headers={
        "x-gateway-accept": "text/event-stream"
    }
)

@timeit
def get_num_tokens_from_messages(content,chat_history=None,model_name=MODEL_NAME_QWEN2HALF_7B):
    llm = None
    if model_name == MODEL_NAME_QWEN2HALF_7B :
        llm = llm_qwen2half_7b
    if model_name == MODEL_NAME_QWEN2HALF_32B:
        llm = llm_qwen2half_32b
    messages = []
    if chat_history:
        messages += [HumanMessage(message['content']) if message['role'] == 'user' else AIMessage(message['content']) for message in chat_history] 
    messages.append(
        HumanMessage(content)
    )
    token_nums = llm.get_num_tokens_from_messages(messages=messages)
    return token_nums  
    

@timeit
def post_api_for_llm(
    content, chat_history=None, model_name=MODEL_NAME_QWEN2HALF_7B,**kwargs
):
    """Post API for LLM
    Args:
        content (str):  Input text for LLM.
        chat_history (list, optional): Previous chat history. Defaults to None.
    Returns:
        str: Response from LLM.
    """
    llm = None
    if model_name == MODEL_NAME_QWEN2HALF_7B :
        llm = llm_qwen2half_7b
    if model_name == MODEL_NAME_QWEN2HALF_32B:
        llm = llm_qwen2half_32b
    messages = []
    if chat_history:
        messages += [HumanMessage(message['content']) if message['role'] == 'user' else AIMessage(message['content']) for message in chat_history] 
    messages.append(
        HumanMessage(content)
    )   
    # response = llm.invoke(messages)
    trace_id = kwargs.get("trace_id")
    user_id = kwargs.get("user_id")
    session_id = kwargs.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    module_name = kwargs.get("module_name")

    config = {
        "callbacks": [langfuse_handler],
        "run_id": trace_id, # trace_id
        "run_name": module_name,
        "metadata": {
            "langfuse_session_id": session_id, # session_id
            "langfuse_user_id": user_id # 记录user_id
        }
    }
    chain = llm | StrOutputParser()
    content = chain.invoke(messages,config=config)
    return content


@timeit
def post_api_for_llm_batch(prompts, model_name=MODEL_NAME_QWEN2HALF_7B,max_concurrency=None,**kwargs):
    """Post API for LLM
    Args:
        content (str):  Input text for LLM.
        chat_history (list, optional): Previous chat history. Defaults to None.
    Returns:
        str: Response from LLM.
    """
    llm = None
    if model_name == MODEL_NAME_QWEN2HALF_7B :
        llm = llm_qwen2half_7b
    if model_name == MODEL_NAME_QWEN2HALF_32B:
        llm = llm_qwen2half_32b

    trace_id = kwargs.get("trace_id")
    user_id = kwargs.get("user_id")
    session_id = kwargs.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    module_name = kwargs.get("module_name")

    config = {
        "callbacks": [langfuse_handler],
        "run_id": trace_id, # trace_id
        "run_name": module_name,
        "metadata": {
            "langfuse_session_id": session_id, # session_id
            "langfuse_user_id": user_id, # 记录user_id
        },
    }
    chain = llm | StrOutputParser()
    if max_concurrency:
        # response = llm.batch(prompts,config={"max_concurrency": max_concurrency})
        config['max_concurrency'] = max_concurrency
        responses = chain.batch(prompts,config=config)
    else:
        responses = chain.batch(prompts,config=config)
    # return [r.content for r in response]
    return responses


@timeit
def apost_api_for_llm(content, chat_history=None, model_name=MODEL_NAME_QWEN2HALF_32B,**kwargs):
    """Post API for LLM
    Args:
        content (str):  Input text for LLM.
        chat_history (list, optional): Previous chat history. Defaults to None.

    Returns:
        str: Response from LLM.
    """
    llm = None
    if model_name == MODEL_NAME_QWEN2HALF_7B :
        llm = llm_qwen2half_7b_stream
    if model_name == MODEL_NAME_QWEN2HALF_32B:
        llm = llm_qwen2half_32b_stream

    messages = []
    if chat_history:
        messages += chat_history
    messages.append({"role": "user", "content": content})
    # response = client.chat.completions.create(
    #     model=model_name, messages=messages, temperature=0, stream=True
    # )

    # for s in response:
    #     yield s.choices[0].delta.content
    trace_id = kwargs.get("trace_id")
    user_id = kwargs.get("user_id")
    session_id = kwargs.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    module_name = kwargs.get("module_name")

    config = {
        "callbacks": [langfuse_handler],
        "run_id": trace_id, # trace_id
        "run_name": module_name,
        "metadata": {
            "langfuse_session_id": session_id, # session_id
            "langfuse_user_id": user_id, # 记录user_id
        },
    }
    chain = llm | StrOutputParser()
    for chunk in chain.stream(messages,config=config):
        yield chunk
    # for chunk in llm.stream(messages,config=config):
    #     yield chunk.content



if __name__ == "__main__":

    from configs.model_config import QA_PROMPT

    QA_PROMPT = """
给你一段长文本：```{context}```
从上面的文本中提取出问答对，忽略句子的序号。
如果无法从中得到答案，请扮演以下角色：
你是一名专家，擅长创作适合的知识问答
以qa对的json数组格式返回结果
问题答案对数量：{num}个
返回结果格式要求：```[{{"问题":"你是谁","答案":"我是小天"}},{{"问题":"今天星期几","答案":"星期三"}}]```
"""

    context = """
问题12：管理员端权限范围中，为什么有些柜组没有显示？
1.深度数字化专柜不显示，可以通过09报表“是否数字化专柜”获知；
2.柜组合同无效，可以在R3系统查询。
3.管理员权限范围选择的品类与柜组所在的品类不一致。
4.管理员选择整个品类时该柜组尚未满足显示条件，请搜索柜号后勾选。
5.柜组无在职的导购，可以在crti511查询。

问题13：管理员端在上架销售单时，系统提示“专柜信息有误”，怎么办？
需当前专柜所绑定的导购先登录企业微信，管理员再尝试上架商品。

问题14：管理员端已作废销售单，但销售单作废后状态依然为“上架中”。重新创建销售单并上架，系统提示“该商品已有销售单上架，不能上架多个销售单”，怎么办？
请提供 柜组编码、已作废的销售单ID，反馈至“百货数字化问题沟通群”内。

问题15：管理员端订单管理中，为什么有些订单没有？
管理员权限范围未选择的柜组和深度数字化专柜订单不在订单管理中。

问题16：柜组已经撤柜，订单尚未处理完毕或者顾客发起退货，管理员如何处理？
方法1：柜组撤柜后，管理员端会接收到该柜组未处理完毕订单/退货订单的提醒，管理员可以在订单管理中处理。
方法2：管理员可以登录大后台，在订单—百货销售订单/百货售后订单，查看和操作订单。
"""

    # context = """
    # 本机关提供政府信息不收取费用。但是，申请人申请公开政府信息的数量、频次明显超过合理范围的，本机关将按照《国务院办公厅关于印发〈政府信息公开信息处理费管理办法〉的通知》（国办函〔2020〕109号）、《重庆市财政局重庆市发展和改革委员会关于政府信息公开信息处理费征收管理有关工作的通知》（渝财综〔2021〕3号）规定收取信息处理费。
    # """
    # prompt = QA_PROMPT.format(context=context, num=num)
    # prompt = QA_PROMPT.format(context=context, num=5)
    # res = post_api_for_llm(content=prompt)
    # print(res)

    # for i, chunk in enumerate(apost_api_for_llm(content=prompt)):
    #     print(i, chunk)

    # print(llm.invoke("你是谁").content)

    # ab = ["你是谁", "你可以做什么"]
    # resps = post_api_for_llm_batch(ab)
    # print(resps)
    
    
    history = [
        {"role": "user","content": "你是谁"},
        {"role": "assistant","content": "我是Qwen，由阿里云开发的大型语言模型。我被设计用来协助人们进行各种文本相关的任务和提供信息。有什么我可以帮助你的吗？"}
    ]
    q = '你可以做什么?'
    print(post_api_for_llm(q,chat_history=history))
    
    print(get_num_tokens_from_messages(q,chat_history=history))
