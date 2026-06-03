"""評価関連スキーマ"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EvaluationResponse(BaseModel):
    """個別回答の評価"""
    id: str
    interview_question_id: str
    overall_score: float
    content_score: float
    structure_score: float
    language_score: float
    passion_score: float
    manners_score: float
    content_feedback: str
    structure_feedback: str
    language_feedback: str
    improvement_suggestions: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggested_answer_points: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerEvaluationRequest(BaseModel):
    """回答評価リクエスト（LLM評価のためのデータ）"""
    question_text: str
    answer_text: str
    question_category: str = ""
    target_company: str = ""
    target_industry: str = ""
    is_japanese: bool = True


class EvaluationDetailResponse(BaseModel):
    """各評価軸の詳細"""
    category: str
    score: float
    feedback: str
    details: str = ""


class BatchEvaluationResponse(BaseModel):
    """面接完了時の一括評価結果"""
    overall_score: float
    content_score: float
    structure_score: float
    language_score: float
    passion_score: float
    manners_score: float
    feedback_summary: str
    improvement_tips: str
    question_evaluations: List[EvaluationResponse] = []
