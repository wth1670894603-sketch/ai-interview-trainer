"""質問モデル — 面接質問バンク"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Enum as SAEnum
import enum

from ..database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class QuestionCategory(str, enum.Enum):
    SELF_PR = "self_pr"                # 自己PR
    GAKUCHIKA = "gakuchika"            # 学生時代に力を入れたこと
    MOTIVATION = "motivation"           # 志望動機
    WEAKNESS = "weakness"               # 短所・改善点
    FUTURE = "future"                   # 将来像・キャリアプラン
    REVERSE_QUESTION = "reverse_q"      # 逆質問
    CASE = "case"                       # ケース面接
    GD = "gd"                           # グループディスカッション
    GENERAL = "general"                 # 一般質問
    OTHER = "other"                     # その他


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(SAEnum(QuestionCategory), nullable=False, index=True)
    difficulty = Column(SAEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    text_ja = Column(Text, nullable=False)       # 日本語質問文
    text_en = Column(Text, default="")           # 英語訳（留学生向け）
    target_company = Column(String(200), default="")  # 特定企業向け（空欄=汎用）
    target_industry = Column(String(200), default="") # 特定業界向け
    target_position = Column(String(200), default="") # 特定職種向け
    purpose = Column(Text, default="")           # この質問の意図
    tips = Column(Text, default="")              # 回答のポイント
    expected_duration_seconds = Column(Integer, default=60)
    order_index = Column(Integer, default=0)     # ソート用
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=_utcnow)

    def __repr__(self):
        return f"<Question {self.category.value}: {self.text_ja[:30]}>"
