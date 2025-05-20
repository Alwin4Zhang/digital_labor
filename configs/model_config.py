import os
import sys
# import logging
import uuid
# import torch

# import torch.cuda
# import torch.backends

# sys.path.append('./')
# from configs.apollo_config import *

# LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"

# # logging.basicConfig(format=LOG_FORMAT)
# logging.basicConfig(
#     filename="./app.log",  # Specify the log file name
#     filemode="a",
#     level=logging.INFO,  # Set the logging level to INFO
#     format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
# )
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# 在以下字典中修改属性值，以指定本地embedding模型存储位置
# 如将 "text2vec": "GanymedeNil/text2vec-large-chinese" 修改为 "text2vec": "User/Downloads/text2vec-large-chinese"
# 此处请写绝对路径
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "/rainbow/model/pytorch/text2vec-large-chinese",
    "m3e-small": "/rainbow/model/pytorch/m3e-small",
    "m3e-base": "/rainbow/model/pytorch/m3e-base",
    "m3e-large": "/rainbow/model/pytorch/m3e-large",
    "bge-large": "/rainbow/model/pytorch/bge-large-zh-v1.5",
    "bge-reranker-large": "/rainbow/model/pytorch/bge-reranker-large",
    "document-segmentation": "/rainbow/model/pytorch/nlp_bert_document-segmentation_chinese-base",
}

# Embedding running device
# EMBEDDING_DEVICE = (
#     "cuda"
#     if torch.cuda.is_available()
#     else "mps" if torch.backends.mps.is_available() else "cpu"
# )
EMBEDDING_DEVICE = "cpu"

embed_model_triton_service_dict = {
    "bge-large": "bge_feature_ensemble",
    "bge-rerank-large": "bge_rerank_ensemble",
    "bge-m3": {"model_name": "bge_m3_ensemble", "output_name": "sentence_embedding"},
}

# Embedding and Rerank model name

EMBEDDING_MODEL = "bge-large"
RERANK_MODEL = "bge-rerank-large"

# RERANK_INSTRUCTION = "为这个句子生成表示以用于检索相关文章："
TITLE_WEIGHT = 0.9

# 本地存放的baichuan ft模型位置
# BAICHUAN_FT_DIR = 'baichuan_ft/'
# FREEZE_DIR = "freeze/"

# LLM lora path，默认为空，如果有请直接指定文件夹路径
LLM_LORA_PATH = ""
USE_LORA = True if LLM_LORA_PATH else False

# LLM streaming reponse
STREAMING = True

# Use p-tuning-v2 PrefixEncoder
USE_PTUNING_V2 = False

# LLM running device
# LLM_DEVICE = (
#     "cuda"
#     if torch.cuda.is_available()
#     else "mps" if torch.backends.mps.is_available() else "cpu"
# )
LLM_DEVICE = "cpu"

# 知识库默认存储路径，默认使用faiss本地存储
KB_ROOT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "knowledge_base"
)

# 基于上下文的prompt模版，请务必保留"{question}"和"{context}"
PROMPT_TEMPLATE = """已知信息：
{context} 

根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}"""

# 请把下面的内容复述出来，必须保证句子的通顺性：
# 保留其中的时间、地点、人物等重要信息：
CHATGLM_PROMPT_TEMPLATE = """请把下面的内容复述出来，必须保证句子的通顺性，保持原有的格式输出：
{context}
""".strip()

CHATGLM3_PROMPT_TEMPLATE = """给你一个示例：\n
问题："我是小天，一个灵智在2023年创造的智能助手？"\n
它的答案是：我是小天，一个灵智在2023年创造的智能助手。\n\n
下面我会再给你一个问题：
问题：{context}\n
它的答案是：
""".strip()

QWEN_PROMPT_TEMPLATE = """输入："我是小天，一个灵智在2023年创造的智能助手？"\n
它原样输出的结果是：我是小天，一个灵智在2023年创造的智能助手。\n\n
下面我会再给你一个问题：输入：{context}\n
它原样输出的结果是：
""".strip()

CHATGLM3_RETELL_PROMPT_TEMPLATE = """你是一个擅于润色文本的专家，请对问题的答案进行润色，生成口语化的表达,不允许修改文本原始的含义，不允许修改其中的数值和英文。\n问题是：{question}\n对应的答案是:{answer}"""

# 缓存知识库数量
CACHED_VS_NUM = 1

# 文本分句长度
# SENTENCE_SIZE = 100
SENTENCE_SIZE = 1000

# 匹配后单段上下文长度
CHUNK_SIZE = 500

# 传入LLM的历史记录长度
LLM_HISTORY_LEN = 3

# 知识库检索时返回的匹配内容条数
VECTOR_SEARCH_TOP_K = 10
# VECTOR_SEARCH_TOP_K = 1

# 知识检索内容相关度 Score, 数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
# VECTOR_SEARCH_SCORE_THRESHOLD = 450 # faiss
VECTOR_SEARCH_SCORE_THRESHOLD = 0.75  # milvus
CHUNK_VECTOR_SEARCH_SCORE_THRESHOLD = 0.43
# VECTOR_SEARCH_SCORE_THRESHOLD = 1

NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

FLAG_USER_NAME = uuid.uuid4().hex

# 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = True

# 是否开启中文标题加强，以及标题增强的相关配置
# 通过增加标题判断，判断哪些文本为标题，并在metadata中进行标记；
# 然后将文本与往上一级的标题进行拼合，实现文本信息的增强。
ZH_TITLE_ENHANCE = False

# 默认的数据库
SQL_FILE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "db"
)


# 数字员工2.0 优化Prompt配置
# 判断跨意图提示词
ACROSS_INTENT_PROMPT = """
INSTRUCTION

你是一个擅于判断用户输入内容是否跨意图的专家，在给定的多轮对话内容可以判断出当前用户是否跨意图，给出结果，只能从```是、否```中选择一个。

INSTANCES
对话示例1: 
对话内容： A:我要查社保规定 B:湖南地区的社保内容如下：.....
		 A:我要查北京的   
当前用户是否跨意图：否

对话示例2: 
对话内容： A:今天星期几 B:星期三
         A:1+1=   
当前用户是否跨意图：是

对话示例3: 
对话内容： A:天虹是什么 B:天虹商城股份有限公司是一家上市公司，深交所，股票代码是...
		 A:灵智和天虹的关系
当前用户是否跨意图：否

接下来有一个新的多轮对话内容:
对话内容： {context}

注意:
1. 如果当前问题是问候语,如"早上好"、"你好"、"晚上好"等，直接回复"是"。

当前用户是否跨意图："""


ACROSS_INTENT_PROMPT = """# Role
你是一个擅于判断用户输入内容是否跨意图的专家，在给定的多轮对话内容可以判断出当前用户是否跨意图，给出结果，只能从```是、否```中选择一个。

# Examples

## Example1:

对话内容：
Q1:我要查社保规定 
A1:湖南地区的社保内容如下：.....
Q2:我要查北京的   

当前用户是否跨意图：否

## Example2

对话内容： 
Q1:今天星期几 
A1:星期三
Q2:1+1=   

当前用户是否跨意图：是

## Example3

对话内容： 
Q1:天虹是什么 
A1:天虹商城股份有限公司是一家上市公司，深交所，股票代码是...
Q2:灵智和天虹的关系

当前用户是否跨意图：否

## Example4
对话内容：
Q1: 工程系列职称，哪些专业可以申报
A1: 根据《中国航空工业集团有限公司工程系列职称评审细则》中的规定，工程系列职称可以申报的专业包括但不限于以下几类：\n\n1. 体系技术专业\n2. 飞行器技术专业\n3. 航电技术专业\n4. 机电技术专业\n5. 飞行控制技术专业\n6. 武器技术专业\n7. 动力技术专业\n8. 航空制造技术专业\n9. 航空材料技术专业\n10. 试验与试飞技术专业\n11. 基础与共性技术专业\n12. 前沿技术专业\n13. 技术管理专业\n14. 其他工程技术专业\n\n这些专业适用于从事相关专业的研究、设计、制造、工艺、试验、验证、定型/鉴定/符合性验证、测试、技术开发、维护、修理等领域的工程技术人员。具体申报条件和要求请参照细则中的相关规定。\n
Q2: 飞行器技术专业包括哪些？
A2: 根据提供的文件内容，飞行器技术专业包括以下具体专业：\n\n- 飞行器总体\n- 空气动力（含水动力、载荷）\n- 进排气系统\n- 结构（含热结构、热防护）\n- 强度（含静、动、疲劳强度，振动与噪声）\n- 旋翼系统\n- 隐身\n- 高超声速飞行器专用技术\n- 特种飞机专用技术\n- 无人机系统\n\n这些专业涵盖了飞行器技术领域的多个方面。
Q3: 申报这个职称，需要满足什么条件？

当前用户是否跨意图：否

# Constrains:
1. 如果当前问题是问候语,如"早上好"、"你好"、"晚上好"等，直接回复"是"。

# Instruction
接下来有一个新的多轮对话内容:
对话内容： {context}

当前用户是否跨意图："""

# ACROSS_INTENT_PROMPT = """
# INSTRUCTION

# 你是一个擅于判断用户输入内容是否跨意图的专家，在给定的多轮对话内容可以判断出当前用户是否跨意图，给出结果，只能从```是、否```中选择一个。

# INSTANCES
# 对话示例1: 

# 对话内容： 
# ```json
# [
#     {{"role":"user","content":"我要查社保规定"}},
#     {{"role":"assistant","content":"湖南地区的社保内容如下：....."}},
#     {{"role":"user","content":"我要查北京的"}},
# ]
# ```
# 当前用户是否跨意图：否

# 对话示例2: 

# 对话内容：

# ```json
# [
#     {{"role":"user","content":"今天星期几"}},
#     {{"role":"assistant","content":"星期三"}},
#     {{"role":"user","content":"1+1="}},
# ]
# ```
# 当前用户是否跨意图：是

# 对话示例3: 

# 对话内容：

# ```json
# [
#     {{"role":"user","content":"天虹是什么"}},
#     {{"role":"assistant","content":"天虹商城股份有限公司是一家上市公司，深交所，股票代码是..."}},
#     {{"role":"user","content":"灵智和天虹的关系"}},
# ]
# ```
# 当前用户是否跨意图：否

# 接下来有一个新的多轮对话内容:
# 对话内容： {context}

# 注意:
# 1. 如果当前问题是问候语,如"早上好"、"你好"、"晚上好"等，直接回复"是"。

# 当前用户是否跨意图："""


# 没有相关信息
DOC_QA_PROMPT_TEMPLATE = """请根据以下公司规定回答问题，如果包含图片链接请原样输出图片链接，不允许修改图片链接内容。如果没有包含相关信息，则回复"这个问题暂时未覆盖，数字员工还在学习升级中，敬请期待~可以先问我其他问题试试哦！"。

{doc_content}
问题：{question}
"""

DOC_QA_PROMPT_TEMPLATE = """请根据以下公司规定回答问题，如果包含图片链接请原样输出图片链接，不允许修改图片链接内容。如果没有包含相关信息，则回复"没有相关信息"。

{doc_content}
问题：{question}
"""

DOC_QA_PROMPT_TEMPLATE2 = """请根据以下公司规定回答问题，如果包含图片链接请原样输出图片链接，不允许修改图片链接内容。答案也可能出现在上一轮的答案中。如果没有包含相关信息，则回复"这个问题暂时未覆盖，数字员工还在学习升级中，敬请期待~可以先问我其他问题试试哦！"。

{doc_content}

上一轮的问题：{last_question}
上一轮的答案: {last_answer}

问题：{question}
"""

DEFAULT_NULL_RESPONSE = "没有相关信息"

DEFAULT_RESPONSE = (
    "这个问题暂时未覆盖，数字员工还在学习升级中，敬请期待~可以先问我其他问题试试哦！"
)

# QA生成提示词
QA_PROMPT = """
INSTRUCTIONS

你是一个擅长从文本中提取问答对的专家,如果输入内容过短或没有合适的问答对，就输出"[]"。

CONTEXT
{context}

注意:
1.以qa对的json数组格式返回结果,返回结果格式要求：```[{{"问题":"","答案":""}}]```
2.要求结果只能是中文，做严谨详实有效的回答。
3.问题答案对数量：{num}个
""".strip()


QA_FEW_SHOT_PROMPT = """
INSTRUCTIONS

你是一个擅长从表格中提取问答对的专家,如果输入内容过短或没有合适的问答对，就输出"[]"。

INSTANCES

case1: 
文本内容:\n3.7.4.1 自签订劳动合同之日起,累计工作满一年及以上的员工,均可享受年休假。年休假时间根据员工工龄计算:未满五年者 5 天,满五年未满十年者 7 天,满十年未满二十年者 10 天,满二十年以上者 15 天。员工工龄在年度内跨档时,年休假天数参见下表

规定:
| 入司日期 | 工龄满一年  | 工龄满 5 年 | 工龄满 10 年 | 工龄满 20 年 |
| --- | --- | --- | --- | --- |
| 7 月 31 日以前 | 5 | 7 | 10 | 15 |
| 8 月 1 日—9 月 30 日 | 3 | 6 | 8 | 13 |
| 10 月 1 日—11 月 30 日 | 2 | 6 | 8 | 11 |
| 12 月 1 日—12 月 31 日 | 1 | 5 | 7 | 10 |
注:工龄跨档时的年休假天数依据年度内工龄满周年的月份加权平均计算。公式为:跨档当年年休假天数=1月至入司月份的月数/12*跨档前对应的年休假天数+入司月份至 12月的剩余月数/12*跨档后对应的年休假天数。(入司当月算一个月计)

生成的qa对数是5个，结果是:
```json[{{"问题": "员工年休假的天数如何计算？","答案": "员工年休假的天数根据工龄计算，具体如下：未满五年者 5 天，满五年未满十年者 7 天，满十年未满二十年以上者 10 天，满二十年以上者 15 天。员工工龄在年度内跨档时，年休假天数按照跨档后工龄计算。"}},{{"问题": "跨档后的年休假天数如何计算？","答案": "跨档后的年休假天数计算公式为：跨档当年年休假天数=1月至入司月份的月数/12*跨档前对应的年休假天数+入司月份至 12 月的剩余月数/12*跨档后对应的年休假天数。"}},{{"问题": "工龄满20年，在12月1日-12月31日入职的，有几天年假?","答案": "10天年假。"}},{{"问题": "入司时间在7月31日以前的，工龄5年，有几天年假？","答案": "7天年假。"}},{{"问题": "入司时间在8 月 1 日—9 月 30 日的，工龄一年，有几天年假？","答案": "3天年假。"}}]
```

case2: 
文本内容:\n门店订货操作指导书
3.职责

| 序号 | 岗位 | 职责 |
| --- | --- | --- |
| 1 | 超市事业部采购经理 | 1、负责制定新商品的首批订单，并通知供应商；  2、监控供应商的送货情况，并对未按合同要求送货的  供应商进行处罚；3、反馈门店提供的供应商不良情况的处罚意见。  |
| 2 | 物流中心 | 负责根据门店的订货商品信息、需求量按时发货。 |
| 3 | 超市片区总经理 | 负责监管片区内各门店的库存情况，并督促超市经理及时跟进、处理库存异常情况 。  |
| 4 | 超市分部经理 | 负责监控超市整体库存水平的合理性，了解各品类库存的异常状况，监督超市品类经理与库存经理对商品  开单、验收及陈列量的维护情况是否到位。  |
| 5 | 超市品类经理 | 1、对自营商品的库存合理性负责，定时维护标准包装商品在订货模块中的陈列量，保障自动要货数量的合理性;  2、负责统仓统配、直上柜、日配商品的手工订货、审核、货源跟进工作。  |
| 6 | 超市库存经理 | 负责审核自动补货商品的订货单，查询、处理门店断 缺货未产生要货单商品，维护及处理系统中的商品信息；组织和监督验货组员工验收商品。  |
| 7 | 超市各品类营业员 | 负责商品库存的盘点，需手工补货时，在终端机上进行要货处理。  |
| 8 | 超市验货营业员 | 根据订货单商品信息，验收物流中心、供应商配送到门店的商品。 |

生成的qa对数是4个，结果是:
```json[{{"问题": "超市采购经理的主要职责是什么？","答案": "超市采购经理的主要职责包括制定新商品的首批订单，监控供应商的送货情况，并对未按合同要求送货的供应商进行处罚；反馈门店提供的供应商不良情况的处罚意见。"}},{{"问题": "物流中心员工的职责是什么？", "答案": "物流中心员工的职责是根据门店的订货商品信息、需求量按时发货。"}},{{"问题": "谁负责监管片区各门店的库存情况，督促超市经理跟进处理库存异常?","答案": "超市片区总经理。"}},{{"问题": "超市验货营业员的主要工作内容是什么？","答案": "根据订货单商品信息，验收物流中心、供应商配送到门店的商品。"}}]
```

现在给你一个文本，要求必须以qa对json数组格式返回结果。
文本内容：\n{context}

注意：
1.要求结果只能是中文，做严谨详实有效的回答，不要原样输出
2.问答对的内容只能与给定的文本内容相关，不允许随意捏造
3.生成的qa对是{num}个
""".strip()


# sprag的auto context，生成全文的提示性摘要，1-2句话
SPRAG_AUTO_CONTEXT_PROMPT = """
INSTRUCTIONS

以下文档是什么？它是关于什么的？ 

你的回答应该是一个句子，并且不应该是一个过长的句子。不要用其他任何东西来回应。 

您必须在回复中包含文档名称（如果有），因为这是一条关键信息。文档名称应尽可能具体和详细。如果有可用的信息，您甚至可以添加作者姓名或出版日期等信息。不要只使用文件名作为文档名称。它需要是一个描述性且人类可读的名称。

您的回复应采用“本文档是：X，内容是关于：Y”的形式。例如，如果该文档是一本关于美国历史的书，名为《美国人民的历史》，您的回答可能是“此文档是：美国人民的历史，并且是关于美国的历史”，涵盖从 1776 年至今的时期。”如果该文件是 Apple Inc. 的 2023 年 10-K 表格，您的回答可能是“本文件是：Apple Inc. 2023 财年 10-K 表格，内容是：Apple Inc. 在本财年的财务业绩和运营情况2023 年。

DOCUMENT
filename: {document_title}

{document}
""".strip()

MAX_TOKENS=32768


# 搜索展开
SEARCH_EXPANSION_PROMPT = """
您是一个查询生成系统。请根据提供的用户输入生成一个或多个搜索查询（最多为 {max_queries}）。不生成答案，仅生成查询。 您生成的每个查询都将用于在知识库中搜索可用于响应用户输入的信息。确保每个查询足够具体以返回相关信息。如果多条信息有用，您应该生成多个查询，每个查询对应所需的每一条特定信息。
""".strip()

SECTION_SUMMARIZE_PROMPT = """
INSTRUCTIONS

你是一个擅长对文档片段内容做总结的助手。

你的回答应该是一个句子，并且不应该是一个过长的句子。不要用其他任何东西来回应。 

DOCUMENT
文件名称: {document_title}

文档片段: {chunk_text}
""".strip()


SECTION_SUMMARIZE_PROMPT = """
INSTRUCTIONS

你是一个擅长对文档片段内容做总结的助手。

你的回答应该几个关键词。不要用其他任何东西来回应。 

DOCUMENT
文件名称: {document_title}

文档片段: {chunk_text}
""".strip()

REWRITE_QUESTION_PROMPT = """
INSTRUCTIONS
        
你是一个擅长对给定的历史对话记录整理成问题的专家。根据历史对话记录，重写用户当前的问题。

HISTORY
{history_context}

当前的问题:{current_question}

注意：
1.请一句话重写用户当前的问题，要求只输出问题
2.着重关注最近3轮对话
""".strip()

GREETING_QUESTION_PROMPT = """
INSTRUCTIONS

你是一个擅长回复问候语的助手。

你的回答应该是一个句子，并且不应该是一个过长的句子。如果不是问候语，则回复\"{default_response}\"。

QUESTION
{question}
""".strip()


CRAG_PROMPT = """
INSTRUCTIONS
您是一名擅长评分的专家，可以给定的文档与用户问题的相关性，答案只能从```是、否```中选择一个。\n 

这是检索到的文档：
{context}

这是用户问题：{question} \n 

注意：
1.不需要输出原因

""".strip()

# DEFAULT_MILVUS_KB_NAME = "digital_labor_avic"
# DEFAULT_ELASTICSEARCH_KB_NAME = "digital_labor_avic"
# DEFAULT_MILVUS_CHUNK_DB_NAME = "digital_labor_chunk_avic"

use_local = os.environ.get("use_local") if os.environ.get("use_local") else False

# if os.environ.get("run_env", "sit").lower() == "uat":
#     logger.info("current env...:{0}".format(os.environ.get("run_env", "sit")))
#     DEFAULT_MILVUS_KB_NAME = "uat_digital_labor_avic"
#     DEFAULT_ELASTICSEARCH_KB_NAME = "uat_digital_labor_avic"

# langfuse里面存的若干提示词
SPRAG_AUTO_CONTEXT_PROMPT_NAME="sprag_auto_context_prompt" # sprag文档综述提示词
SECTION_SUMMARIZE_PROMPT_NAME="section_summarize_prompt" # 片段关键词生成提示词
REWRITE_QUESTION_PROMPT_NAME="rewrite_question_prompt" # 多轮对话问题重写提示词
CRAG_PROMPT_NAME="crag_prompt" # crag提示词，判断chunk和问题是否相关
GREETING_QUESTION_PROMPT_NAME = "greeting_question_prompt" # 兜底回复提示词
QA_FEW_SHOT_PROMPT_NAME_NAME="qa_few_shot_prompt" # 表格数据few-shot提示词
QA_PROMPT_NAME="qa_prompt" # QA生成提示词
DOC_QA_PROMPT_TEMPLATE_NAME="doc_qa_prompt_template" # RAG问答提示词
ACROSS_INTENT_PROMPT_NAME = "across_intent_prompt" # 对话是否跨意图提示词
HYDE_PROMPT_NAME = "hyde_prompt" # HyDE提示词

# 问题拆解模块
QUERY_DECOMPOSITION_NAME = "query_decomposition_prompt"
DECOMPOSED_QUESIONTS_TO_ANSWER_NAME = "decomposed_questions_to_answer_prompt"
REASON_FINAL_ANSWER_NAME = "reason_final_answer_prompt"

# 查询扩展，默认将问题扩展5个问题
QUERY_EXPAND_NAME ="query_expand_prompt" 

# 实体识别
QUERY_EXTRACT_METADATA_FIELDS_NAME = "extract_metadata_field_prompt"
