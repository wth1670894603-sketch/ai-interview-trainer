"""ES（エントリーシート）モデル"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from ..database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class ESCategory(str, enum.Enum):
    GAKUCHIKA = "gakuchika"    # 学生時代に力を入れたこと
    SELF_PR = "self_pr"        # 自己PR
    MOTIVATION = "motivation"  # 志望動機
    OTHER = "other"            # その他


class ES(Base):
    """エントリーシート"""
    __tablename__ = "entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), default="")                        # タイトル
    category = Column(SAEnum(ESCategory), nullable=False)           # カテゴリ
    content = Column(Text, nullable=False)                          # ES本文
    target_company = Column(String(200), default="")               # 志望企業（任意）
    target_position = Column(String(200), default="")              # 志望職種（任意）
    created_at = Column(DateTime, default=_utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<ES {self.category.value}: {self.title[:30]}>"
