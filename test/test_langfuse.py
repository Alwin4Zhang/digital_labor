import sys
import uuid

sys.path.append("./")

from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

from utils.traceback import langfuse,langfuse_handler
from utils.llm_util import llm_qwen2half_32b,llm_qwen2half_7b,post_api_for_llm,post_api_for_llm_batch


across_intent_prompt = langfuse.get_prompt("across_intent_prompt")
# print(across_intent_prompt.prompt)

context = """
Q1:你是谁
A1:我是小天
Q2:hello
"""

prompt = across_intent_prompt.compile(context=context)
print(prompt)

chain = llm_qwen2half_7b | StrOutputParser()

predefined_run_id = str(uuid.uuid4())
print(predefined_run_id)

# chain.invoke(prompt, 
#         config={
#             "callbacks": [langfuse_handler],
#             "run_id": predefined_run_id, # trace_id
#             # "run_name": "Famous Person Locator3",
#             "metadata": {
#                 "langfuse_session_id": "test-session-id9", # session_id
#                 "langfuse_user_id": "157212" # 记录user_id
#             }
#     })
prompt = "你是谁"
chunks = chain.stream(prompt, 
        config={
            "callbacks": [langfuse_handler],
            "run_id": predefined_run_id, # trace_id
            # "run_name": "Famous Person Locator3",
            "metadata": {
                "langfuse_session_id": "test-session-id9", # session_id
                "langfuse_user_id": "157212" # 记录user_id
            }
    })

for chunk in chunks:
    print(chunk)

# cnt = post_api_for_llm(
#     content="列举几个国家的名称",
#     trace_id="123456",
#     user_id='157212',
#     session_id=predefined_run_id,
#     module_name="test-module"
# )
# print(cnt)

prompts = [
    "你是谁",
    "列举一些国家"
]

# resps = post_api_for_llm_batch(prompts=prompts,
#                                trace_id="456789",
#                                user_id='157212',
#                                session_id=predefined_run_id,
#                                module_name="test-module",
#                                max_concurrency=2)
# print(resps)