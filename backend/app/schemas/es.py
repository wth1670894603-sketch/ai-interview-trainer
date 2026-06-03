"""ES関連スキーマ"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ESCreate(BaseModel):
    """ES登録"""
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(...)  # gakuchika / self_pr / motivation / other
    content: str = Field(..., min_length=10)
    target_company: str = ""
    target_position: str = ""


class ESResponse(BaseModel):
    """ES情報"""
    id: str
    title: str
    category: str
    content: str
    target_company: str
    target_position: str
    created_at: datetime

    class Config:
        from_attributes = True


class ESGeneratedQuestion(BaseModel):
    """ESから生成された質問"""
    question_text: str
    purpose: str = ""
    tips: str = ""


class ESGenerateResponse(BaseModel):
    """ESからの質問生成結果"""
    es_id: str
    questions: List[ESGeneratedQuestion]
