"""評価モデル — 各回答の詳細評価"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ..database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Evaluation(Base):
    """個別質問への評価"""
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_question_id = Column(
        String(36), ForeignKey("interview_questions.id"),
        nullable=False, unique=True, index=True
    )

    # 総合スコア（100点満点）
    overall_score = Column(Float, default=0.0)

    # 各軸スコア
    content_score = Column(Float, default=0.0)      # 内容
    structure_score = Column(Float, default=0.0)    # 構成
    language_score = Column(Float, default=0.0)     # 日本語力
    passion_score = Column(Float, default=0.0)      # 熱意
    manners_score = Column(Float, default=0.0)      # マナー

    # 詳細フィードバック
    content_feedback = Column(Text, default="")      # 内容に対する具体的フィードバック
    structure_feedback = Column(Text, default="")    # 構成の評価
    language_feedback = Column(Text, default="")     # 日本語の改善点
    improvement_suggestions = Column(Text, default="")  # 改善提案

    # AIの評価詳細（構造化データ）
    strengths = Column(JSON, default=list)           # ["説得力がある", "具体例が良い"]
    weaknesses = Column(JSON, default=list)          # ["結論が曖昧", "時間が長い"]
    keywords_missed = Column(JSON, default=list)     # 入れられたが入ってないキーワード
    suggested_answer_points = Column(JSON, default=list)  # 模範回答のポイント

    # 生成メタ情報
    model_used = Column(String(100), default="")
    evaluation_duration_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=_utcnow)

    # リレーション
    interview_question = relationship("InterviewQuestion", back_populates="evaluation")

    def __repr__(self):
        return f"<Evaluation {self.overall_score:.1f}/100>"


class EvaluationDetail(Base):
    """評価の生データ（LLM出力のJSON丸ごと保存）"""
    __tablename__ = "evaluation_details"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    evaluation_id = Column(
        String(36), ForeignKey("evaluations.id"),
        nullable=False, index=True
    )
    raw_prompt = Column(Text, default="")
    raw_response = Column(JSON, default=dict)
    created_at = Column(DateTime, default=_utcnow)

    def __repr__(self):
        return f"<EvaluationDetail for {self.evaluation_id}>"
