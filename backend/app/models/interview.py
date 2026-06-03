"""面接セッションモデル"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from ..database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class InterviewStatus(str, enum.Enum):
    PENDING = "pending"          # 作成済み、未開始
    IN_PROGRESS = "in_progress"  # 進行中
    COMPLETED = "completed"      # 完了
    CANCELLED = "cancelled"      # キャンセル


class InterviewType(str, enum.Enum):
    INDIVIDUAL = "individual"    # 個人面接
    GROUP = "group"              # 集団面接
    GD = "gd"                    # グループディスカッション
    CASE = "case"                # ケース面接
    REVERSE = "reverse"          # 逆質問メイン


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    # 面接設定
    interview_type = Column(SAEnum(InterviewType), default=InterviewType.INDIVIDUAL)
    status = Column(SAEnum(InterviewStatus), default=InterviewStatus.PENDING)
    target_company = Column(String(200), default="")      # 志望企業
    target_industry = Column(String(200), default="")     # 志望業界
    target_position = Column(String(200), default="")    # 志望職種
    major = Column(String(200), default="")              # 学科・専攻
    university = Column(String(200), default="")         # 大学名
    duration_minutes = Column(Integer, default=15)        # 想定時間
    question_count = Column(Integer, default=5)           # 質問数

    # スコア（完了時）
    overall_score = Column(Float, nullable=True)          # 総合スコア
    content_score = Column(Float, nullable=True)
    structure_score = Column(Float, nullable=True)
    language_score = Column(Float, nullable=True)
    passion_score = Column(Float, nullable=True)
    manners_score = Column(Float, nullable=True)

    # フィードバック
    feedback_summary = Column(Text, default="")           # 総評
    improvement_tips = Column(Text, default="")           # 改善点

    # タイムスタンプ
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    # リレーション
    user = relationship("User", back_populates="interviews")
    questions = relationship("InterviewQuestion", back_populates="interview",
                             cascade="all, delete-orphan", order_by="InterviewQuestion.order_index")

    def __repr__(self):
        return f"<Interview {self.id[:8]} ({self.status.value})>"


class InterviewQuestion(Base):
    """面接内の個別質問と回答"""
    __tablename__ = "interview_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=True)

    # 質問内容（定型質問以外の自由質問にも対応）
    question_text = Column(Text, nullable=False)          # 実際の質問文
    question_category = Column(String(50), default="")    # カテゴリ

    # ユーザーの回答
    answer_text = Column(Text, default="")                # 文字起こしテキスト
    answer_audio_path = Column(String(500), default="")   # 録音ファイルパス
    answer_duration_seconds = Column(Float, default=0.0)  # 回答時間

    # 順序
    order_index = Column(Integer, default=0)

    # タイムスタンプ
    started_at = Column(DateTime, nullable=True)          # 回答開始時刻
    answered_at = Column(DateTime, nullable=True)          # 回答完了時刻
    created_at = Column(DateTime, default=_utcnow)

    # リレーション
    interview = relationship("Interview", back_populates="questions")
    evaluation = relationship("Evaluation", uselist=False, back_populates="interview_question",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InterviewQuestion {self.order_index}: {self.question_text[:30]}>"
