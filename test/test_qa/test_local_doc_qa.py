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
 
    
