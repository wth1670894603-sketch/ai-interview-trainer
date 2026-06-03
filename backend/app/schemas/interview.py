"""面接セッション関連スキーマ"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class InterviewCreate(BaseModel):
    """新規面接セッション作成リクエスト"""
    interview_type: str = "individual"
    target_company: str = ""
    target_industry: str = ""
    target_position: str = ""
    major: str = ""
    university: str = ""
    duration_minutes: int = 15
    question_count: int = 5


class InterviewQuestionAnswer(BaseModel):
    """回答提出"""
    answer_text: str = Field(..., min_length=1)
    answer_duration_seconds: float = 0.0


class InterviewQuestionResponse(BaseModel):
    """面接内の個別質問"""
    id: str
    question_text: str
    question_category: str
    order_index: int
    answer_text: str
    answer_duration_seconds: float
    has_evaluation: bool = False

    class Config:
        from_attributes = True


class InterviewResponse(BaseModel):
    """面接セッション詳細"""
    id: str
    interview_type: str
    status: str
    target_company: str
    target_industry: str
    target_position: str
    major: str
    university: str
    duration_minutes: int
    question_count: int
    overall_score: Optional[float] = None
    feedback_summary: str
    questions: List[InterviewQuestionResponse] = []
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewListResponse(BaseModel):
    """面接一覧"""
    interviews: List[InterviewResponse]
    total: int
    page: int
    per_page: int


class InterviewStartResponse(BaseModel):
    """面接開始レスポンス（最初の質問を含む）"""
    interview_id: str
    question: InterviewQuestionResponse
    total_questions: int
