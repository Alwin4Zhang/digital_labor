from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer
from db.base import Base


class BaseModel(Base):
    """基础模型,必备字段"""

    __abstract__ = True

    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID"
    )
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, comment="更新时间")
    created_by = Column(String(50), default=None, comment="创建者")
    updated_by = Column(String(50), default=None, comment="更新者")
    created_name = Column(String(50), default=None, comment="创建者名字")
    updated_name = Column(String(50), default=None, comment="更新者名字")
    deleted = Column(Integer, default=0, comment="是否删除")
    version = Column(Integer, default=0, comment="版本号")

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
