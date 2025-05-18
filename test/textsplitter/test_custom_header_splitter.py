import sys
import json

sys.path.append("./")

from io import BytesIO, StringIO

from loader.unstructured_loaders.pdf_loader import PDFLoader
from loader.unstructured_loaders.doc_loader import DocLoader
from loader.unstructured_loaders.qa_loader import TableLoader
from loader.unstructured_loaders.ppt_loader import PPTLoader
from textsplitter.document_header_splitter import DocumentHeaderTextSplitter
from utils.common import convert_bytes_to_file, convert_file_type

# abs_path = "/rainbow/zhangjunfeng/langchain-ChatGLM/knowledge_base/content/中国反洗钱报告.pdf"
# abs_path = "/rainbow/zhangjunfeng/langchain-ChatGLM/knowledge_base/content/23-天虹商场股份有限公司敏感信息排查管理制度（2010年11月）.pdf"
# pdf_loader = PDFLoader(abs_path)

abs_path = (
    "/rainbow/zhangjunfeng/langchain-ChatGLM/knowledge_base/content/测试文档.docx"
)
# 文件路径测试
# doc_loader = DocLoader(abs_path)

# TODO:文件流测试


def parse_doc_file_with_stream():
    with open(abs_path, "rb") as rf:
        file_stream = BytesIO(rf.read())

    doc_loader = DocLoader(file_path="测试文档.docx", file_stream=file_stream)
    blocks = doc_loader.blocks
    print(blocks)


# parse_doc_file_with_stream()


def parse_pdf_file_with_stream(abs_path):
    with open(abs_path, "rb") as rf:
        file_stream = BytesIO(rf.read())
    doc_loader = PDFLoader(
        file_path="23-天虹商场股份有限公司敏感信息排查管理制度（2010年11月）.pdf",
        file_stream=file_stream,
    )


def parse_ppt_file_with_stream(abs_path):
    with open(abs_path, "rb") as rf:
        file_stream = BytesIO(rf.read())
    doc_loader = PPTLoader(
        file_path="手机自助买单20180904.pptx", file_stream=file_stream
    )


def test_naive_langchain_html_splitter():
    """测试原生的html splitter的效果"""
    from langchain.text_splitter import HTMLHeaderTextSplitter

    headers_to_split_on = [
        ("h1", "Header 1"),
        ("h2", "Header 2"),
        ("h3", "Header 3"),
        ("h4", "Header 4"),
        ("h5", "Header 5"),
        ("h6", "Header 6"),
    ]

    prefix = """
    <!DOCTYPE html>
    <div id="page0">\n"""
    suffix = """\n</div>"""

    total_html = ""
    total_html += prefix
    for block in doc_loader.blocks:
        total_html += block["html"]
    total_html += suffix
    # print(total_html)

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    documents = html_splitter.split_text(total_html)
    print(documents)


if __name__ == "__main__":
    import re
    import sys

    sys.path.append("./")

    from utils.llm_util import post_api_for_llm
    import cv2
    import base64
    import os
    from utils.common import convert_base64_to_buffer, upload_file
    from utils.common import convert_flowchart

    markdown_re = re.compile(r"(\|[:]? [-]+ \|)|(\|[:]?[-]+\|)")  # 匹配markdown的份

    # doc_path = "././test/test_files/华东区执行方案(育儿假、独生子女父母护理假).docx"

    # doc_path = "././test/test_files/出差管理制度规范.docx"
    # print(os.path.abspath(doc_path))

    # doc_path = "././test/test_files/育儿假东南区执行方案（流程版）20220413.docx"
    # doc_path = "././test/test_files/湖南地区育儿假、独生子女父母护理假执行方案.doc"

    tmp_file_path = "././loader/unstructured_loaders/tmp_files"
    # doc_path = convert_file_type(doc_path=doc_path,target_format="docx",output_directory=tmp_file_path)

    # doc_loader = DocLoader(file_path=doc_path, file_stream=None)

    doc_path = "././test/test_files/8.3.1.2.4 收入核算操作指引.pdf"
    doc_path = "././test/test_files/8.3.1.2.1 柜组及库区设置操作规范.pdf"

    # error files
    doc_path = "././test/test_files/3019君尚店装修入场签订资料.docx"
    doc_path = "././test/test_files/生产下载的数据.pdf"
    doc_path = "././test/test_files/小红书节点场景行业洞察报告-小红书_李芳_145556.pdf"

    doc_path = "././test/test_files/2023天虹“中产阶级”人群需求洞察报告.pptx"
    # doc_path = "././test/test_files/性能测试自动化平台使用.pptx"
    doc_path = "././test/test_files/魔镜洞察：2024年一季度消费新潜力白皮书-服饰鞋包_李芳_145556.pdf"

    doc_path = "././test/test_files/6.2.1.0.3 生鲜商品陈列指引A1.pdf"

    import time

    # start = time.time()
    # doc_path = "././test/test_files/9.6.1.1考勤管理制度.docx"
    # # doc_loader = PDFLoader(file_path=doc_path, file_stream=None)
    # doc_loader = DocLoader(file_path=doc_path, file_stream=None)
    # # doc_loader = PPTLoader(file_path=doc_path, file_stream=None)
    # blocks = doc_loader.blocks
    # title = doc_loader.maybe_title
    # print(time.time() - start)

    # document_splitter = DocumentHeaderTextSplitter()
    # docs = document_splitter.split_text(
    #     blocks=doc_loader.blocks,
    #     use_header=False
    # )

    # print(docs)

    # from db.service.knowledge_base_service import (
    #     parse_doc_file_with_stream,
    #     qa_release_valiate,
    # )

    # res, file_type = parse_doc_file_with_stream(doc_path, sprag_enhance=True)

    # from chains.local_hybrid_rag import LocalHybridRag

    # local_hybrid_rag = LocalHybridRag()

    # question = "存货存货与成本核算操作指引质量要求"
    # for resp, history in local_hybrid_rag.dialog_onetune(query=question,chat_history=[]):
    #     print(resp,history)

    docs = [
        {
            "id": "123456",
            "question": "存货存货与成本核算操作指引质量要求",
            "answer": "存货存货与成本核算操作指引质量要求",
            "document_uuid": "123456",
            "filename": "123456.docx",
            "release_status": "qa_await",
        },
        {
            "id": "123457",
            "question": "存货存货与成本核算操作指引质量要",
            "answer": "存货存货与成本核算操作指引质量要求",
            "document_uuid": "123456",
            "filename": "123456.docx",
            "release_status": "qa_await",
        },
        {
            "id": "123458",
            "question": "存货存货与成本核算操作指引质量要求",
            "answer": "存货存货与成本核算操作指引质量要求",
            "document_uuid": "123458",
            "filename": "1234567.docx",
            "release_status": "qa_await",
        },
        {
            "id": "123459",
            "question": "存货存货与成本核算操作指引质量要求",
            "answer": "存货存货与成本核算操作指引质量要求",
            "document_uuid": "123457",
            "filename": "1234568.docx",
            "release_status": "qa_await",
        },
        {
            "id": "123460",
            "question": "知识图谱问答在CCKS上的第四届比赛有哪些要求？",
            "answer": "<p>知识图谱问答在CCKS上的第四届比赛要求参赛选手的问答系统既能处理各种百科类的浅层问题，也能处理具备一定领域知识的啊题。参赛队伍需要按照文档内容含义来理解和回答问题，避免过于肤浅或答案明显的问题。同时，参赛选手的问答系统还需要能够处理生活服务领域的问题，如旅游、酒店、美食等。我们希望参赛选手能够充分利用这些知识图谱，发挥其智能和创造力，为用户提供更加准确、全面和个性化的问答服务。</p>",
            "document_uuid": "1234579",
            "filename": "12345689.docx",
            "release_status": "qa_await",
        },
    ]

    docs = [
        {
            "id": 23010,
            "question": "预算考核与评价流程A1主要关注什么？",
            "answer": "\n预算考核与评价流程a1主要关注公司内部的预算管理流程,包括制定年度考核方案、审批、下发、培训、执行、业绩考核、审批结果、奖金分配、方案优化等环节,以及相关流程的修订记录.\n其目的是确保财务资源的有效利用和管理.",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
        {
            "id": 23011,
            "question": "预算考核与评价流程A1的主要目的是什么？",
            "answer": "\n预算考核与评价流程a1的主要目的是充分调动公司内外部资源,将预算目标与员工日常工作紧密相连,推动和激励员工完成预算目标.",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
        {
            "id": 23012,
            "question": "本文档主要应用于哪个领域？",
            "answer": "\n本文档主要应用于公司的财务管理,具体为预算管理流程中的预算考核与评价.",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
        {
            "id": 23013,
            "question": "预算考核与评价流程适用于哪些部门？",
            "answer": "文档内解析",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
        {
            "id": 23014,
            "question": "预算考核与评价流程A1的流程图在哪里可以找到？",
            "answer": "\n流程图位于附件中,详细展示了预算考核与评价的流程.",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
        {
            "id": 23016,
            "question": "预算考核与评价流程适用于哪些部门？",
            "answer": "文档内新建",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        },
    ]

    docs = [
        {
            "id": 23305,
            "question": "9.7.2员工退休管理规范",
            "answer": "文档内新建",
            "document_uuid": "4d8d3502482811ef86f46705253b7244",
            "filename": "8.1.1.1 预算考核与评价流程A1.pdf",
            "release_status": "qa_await",
        }
    ]
    # from db.service.knowledge_base_service import qa_release_valiate

    # similar_groups = qa_release_valiate(docs=docs)

    # from db.service.knowledge_base_service import qa_generate_to_db

    # document_uuid = "c104690e431b11ef86f46705253b7244"
    # source = '上传'
    # question_type = '财务'
    # created_by = '157000'
    # created_name = '张三'

    # qa_generate_to_db(document_uuid=document_uuid, source=source, question_type=question_type, created_by=created_by, created_name=created_name)

    # q = "财务考核管理流程A1流程的目的是什么？"

    from chains.local_hybrid_rag import LocalHybridRag

    local_hybrid_rag = LocalHybridRag()

    # local_hybrid_rag.dialog_onetune(query=q,chat_history=[])

    # q = {
    #     "question": "超市堆头端架管理规范A1的主要目的是什么？",
    #     "history": [
    #         {
    #             "role": "user",
    #             "content": "超市DM操作流程的管理目的是什么？"
    #         },
    #         {
    #             "role": "assistant",
    #             "content": "通过对dm操作流程的管理,确保运行过程中各部门的协同性,提高dm的效率\n并充分利用dm促销的效果,提升超市的商品与价格竞争力,以带动超市客流及销售."
    #         }
    #     ]
    # }

    # local_hybrid_rag.dialog_onetune(query=q['question'],chat_history=q['history'])

    # query = "湖南地区的"
    # chat_history = [
    #     {"role": "user", "content": "育儿假怎么休"},
    #     {
    #         "role": "assistant",
    #         "content": "育儿假的请休按周年计算,即以子女周岁作为计算年度.",
    #     }
    # ]

    # for resp, history in local_hybrid_rag.dialog_onetune(query, chat_history):
    #     # print(resp, history)
    #     print(resp)

    # q = "补助是多少?"
    # history = [
    #     {"role": "user", "content": "南昌出差期间，普通员工的补助标准是多少？"},
    #     {
    #         "role": "assistant","content": "作为普通员工，你在南昌出差的住宿标准是300元/人/天。根据文档中的附表2:员工国内差旅费标准，其他城市的住宿费标准为300元，南昌属于其他城市类别，因此你的住宿费标准为300元/人/天。同时，你还可以享有100元的补助（含伙食和交通补助）。"
    #     }
    # ]

    # q = "我是部门总监，出差交通补贴标准是多少"
    # q = "天虹请假流程"
    q = "华东地区育儿假审批流程"
    # q = "年休假审批流程"
    q = "婚假审批流程"
    history = [
        {"role": "user", "content": "天虹的请假流程"},
        {
            "role": "assistant",
            "content": """天虹公司的请假流程如下：

1. **病假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/n7s0Uto4njvBFSk4Oh5PW1ax.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/JpsvCXTR3oEASXlnWK2BdIqP.png)

2. **事假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/O1rgyVoNmJqyXhWWYdNtKzTZ.png)

3. **工伤假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/Lp6nFKsO4gybf2GMExtpwPlq.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/jJXjbHoBx3JA32i1EnTLc99f.png)

4. **年休假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/3wONr5AIsoTdlqY4DS0mYeoJ.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/58kZdxgkTsrMG4RvDdvwhVUh.png)

5. **婚假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/8hUpmgrV8QTTy5u0QfHEgAy2.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/kCKOzXfQBCYdJa9YesLz7hk2.png)

6. **产检假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/5abT7ztrTPiHmdVaihvnCWfh.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/GLd6ckGo7MLtmfwXCsfgpREJ.png)

7. **产假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/w4f8lsu9wk6hY2gSzCcaQpz4.png)
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/NOKwkIlVWpXRLuOyC0c0YSL0.png)

8. **流产假**：
   - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/H77985LAM0TnqXDijbV85kBv.png)

9. **哺乳假**：
   - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/YPgtt0VIhOQelaDiMlrd1UOu.png)

10. **看护假**：
    - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/N4OWH7JHbzgCMN3rJRPZll55.png)
    - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/EEoBXp4L13uRZk5UZdJAtnCX.png)

11. **节育假**：
    - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/qcuXbWfLOA3qI7ocDkojAmQS.png)
    - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/r4Y9bv3fYGu0vq1zS8ByZuA4.png)

12. **丧假**：
    - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/VeFPw14BAAzL2nPqHFN24mwe.png)
    - 审批材料：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/VyJ8OcKr5gLnj2ZTi9Xjcy3r.png)

13. **补休**：
    - 审批流程：![](https://assets.tianhong.cn/bigdata/digital-employee/attach/img/2024/8/27/WgH7i5MCpSDAaXcorO8S0hKD.png)

各类假期的申请均需在公司HR系统“员工自助—我要请假”中提交，且需在休假前完成提交审批。如遇紧急情况无法提前办理请假手续，员工或家属需在24小时内以短信、微信等形式通知直接上级，并在假期结束后补办请假手续。""",
        },
    ]
    history = []
    q = "生成式人工智能安全标准"
    start_time = time.time()
    for resp, history in local_hybrid_rag.dialog_onetune(query=q, chat_history=history):
        # print("--" * 10, resp, history)
        print("--" * 10, resp["result"])
    print(time.time() - start_time)
