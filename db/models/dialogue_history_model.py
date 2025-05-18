from sqlalchemy import Column, Integer, String, DateTime, JSON, func

# from sqlalchemy.ext.declarative import declarative_base
from db.models.base import BaseModel

# Base = declarative_base()


class DialogueBaseModel(BaseModel):
    """对话模型"""

    __tablename__ = "dialogue_history"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="对话id")
    query = Column(String(4096), comment="用户问题")
    response = Column(String(4096), comment="回复答案")
    chat_type = Column(String(50), comment="聊天类型")  # 知识库检索/开放问答
    meta_data = Column(
        JSON, default={}, comment="向量索引库中meta_data"
    )  # 记录知识库id等，以便后续扩展关联等

    def __repr__(self) -> str:
        return f"""<DialogueBase(id='{self.id}', question='{self.query}', answer='{self.response}',chat_type='{self.chat_type}')>"""

    # def to_dict(self):
    #     return {
    #         c.name: getattr(self, c.name, None)
    #         for c in self.__table__.columns
    #     }
