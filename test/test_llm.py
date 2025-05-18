

import os
import sys

sys.path.append("./")
import tiktoken
from typing import Tuple
from configs.apollo_config import (
    API_FOR_QWEN2HALF_32B_URL_PREFIX,
    API_FOR_QWEN2HALF_7B_URL_PREFIX,
    MODEL_NAME_QWEN2HALF_32B,
    MODEL_NAME_QWEN2HALF_7B ,
)
from langchain_openai import ChatOpenAI

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
    temperature=0
)

llm_qwen2half_7b = ChatOpenAIIn05(
    model=MODEL_NAME_QWEN2HALF_7B ,
    openai_api_key="EMPTY",
    openai_api_base=API_FOR_QWEN2HALF_7B_URL_PREFIX,
    temperature=0,
    default_headers={
        "x-gateway-accept": "text/event-stream"
    }
)

# print(llm_qwen2half_32b.invoke("你是谁"))

print(llm_qwen2half_7b.invoke("你是谁"))

for chunk in llm_qwen2half_7b.stream("你是谁"):
    print(chunk)