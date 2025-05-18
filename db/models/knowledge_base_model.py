from sqlalchemy import Column, Integer, String, DateTime, JSON, func, VARCHAR
from db.models.base import BaseModel


class KnowledgeBaseModel(BaseModel):
    """知识库模型"""

    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="问题id")
    document_uuid = Column(String(50), comment="所属文档id")
    question = Column(String(128), comment="问题")
    answer = Column(String(4500), comment="答案")
    answer_markdown = Column(String(4500), comment="答案markdown格式")
    question_type = Column(String(32), comment="问题类型:阿波罗配置")
    source = Column(
        String(8),
        default="create",
        comment="问题来源：自建=create ,文件解析=file，默认create",
    )

    release_status = Column(
        String(32), default="qa_await", comment="待发布=qa_await 已发布=qa_released，默认qa_await"
    )
    like_num = Column(Integer, default=0, comment="点赞数")
    dislike_num = Column(Integer, default=0, comment="点踩数")
    chunk_index = Column(String(128), comment="文档块索引")

    # kb_name = Column(String(50), comment='所属知识库名称')

    def __repr__(self):
        return f"""<KnowledgeBase(id='{self.id}', document_id='{self.document_id}',status='{self.status}',question='{self.question}',source='{self.source}', create_time='{self.created_time}')>"""


class DocumentBaseModel(BaseModel):
    """文档解析模型"""

    __tablename__ = "document"

    # id = Column(Integer, primary_key=True, autoincrement=True, comment='文档id')
    id = Column(Integer, primary_key=True, autoincrement=True, comment="文档id")
    document_uuid = Column(String(128), comment="上传文档生成的ID，文档标识，非主键ID")
    # url = Column(String(256), comment='oss url')
    # release_status = Column(
    #     String(8),
    #     default="parsing",
    #     comment="解析中=parsing 学习中=learning 待发布=await 已发布=released，解析失败=fail，默认parsing",
    # )
    
    # 二期更新状态 解析中=parsing，解析成功=parsed QA生成中=qa_generating ，QA待发布=qa_await，QA已发布=qa_released
    release_status = Column(
        String(8),
        default="parsing",
        comment="解析中=parsing 解析成功=parse_succeed QA生成中=qa_generating,QA待发布=qa_await 已发布=qa_released，解析失败=parse_failed，默认parsing",
    )
    upload_status = Column(
        String(32),
        default="uploading",
        comment="文件上传oss云服务器状态：上传中=uploading 成功=success 失败=fail ，默认uploading",
    )
    name = Column(String(256), comment="文档名")
    question_type = Column(
        String(32), comment="问题类型:阿波罗配置"
    )  # 上传文档选定的文档类型
    document_type = Column(String(32), comment="文档类型:ppt pdf word csv xls xlsx tsv...")
    chunks = Column(JSON, default={}, comment="文档chunks")
    # kb_name = Column(String(50), comment='所属知识库名称')
    assets_path = Column(
        String(256),
        comment="上传后含目录的文件名，例如：upload/bbc/sku/2023/5/15/F4RzoW3RMSJSyQcUAm5QgB5b.jpg",
    )
    domain = Column(
        String(128), comment="可访问域名信息，例如：https://dev-assets-api.tianhong.cn/"
    )

    source = Column(
        String(8),
        default="document",
        comment="任务类型：知识问答=knowledge ,文件解析=document，默认document",
    )
    
    def __repr__(self):
        return f"""<DocumentBase(id='{self.id}', document_id='{self.id}',file_name='{self.name}',file_ext='{self.document_type}', create_time='{self.created_time}',source='{self.source}')>"""
