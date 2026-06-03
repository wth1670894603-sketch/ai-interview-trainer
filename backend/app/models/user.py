"""ユーザーモデル"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # プロフィール
    display_name = Column(String(100), default="")
    is_japanese = Column(Boolean, default=True)  # 留学生かどうかの判別
    university = Column(String(200), default="")
    grade = Column(String(50), default="")  # B3, M1 など
    target_industry = Column(String(200), default="")

    # 権限
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # タイムスタンプ
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    # リレーション
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"
