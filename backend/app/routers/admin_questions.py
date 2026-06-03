"""管理者用 質問管理API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.question import Question, QuestionCategory, DifficultyLevel
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/admin/questions", tags=["管理者（質問）"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="管理者権限が必要です")
    return current_user


@router.get("")
def list_questions(
    category: str = "",
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """質問一覧"""
    q = db.query(Question).filter(Question.is_active == 1)
    if category:
        q = q.filter(Question.category == category)
    questions = q.order_by(Question.category, Question.order_index).all()

    return [
        {
            "id": q.id,
            "category": q.category.value,
            "difficulty": q.difficulty.value if q.difficulty else "medium",
            "text_ja": q.text_ja,
            "purpose": q.purpose,
            "tips": q.tips,
            "expected_duration_seconds": q.expected_duration_seconds,
        }
        for q in questions
    ]


@router.post("")
def create_question(
    data: dict,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """質問を追加"""
    max_order = db.query(Question.order_index).filter(
        Question.category == data["category"]
    ).order_by(Question.order_index.desc()).first()
    next_order = (max_order[0] + 1) if max_order else 0

    q = Question(
        category=QuestionCategory(data["category"]),
        difficulty=DifficultyLevel(data.get("difficulty", "medium")),
        text_ja=data["text_ja"],
        purpose=data.get("purpose", ""),
        tips=data.get("tips", ""),
        expected_duration_seconds=data.get("expected_duration_seconds", 90),
        order_index=next_order,
        is_active=1,
    )
    db.add(q)
    db.commit()
    return {"message": "質問を作成しました", "id": q.id}


@router.delete("/{question_id}")
def delete_question(
    question_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """質問を削除（論理削除）"""
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="質問が見つかりません")
    q.is_active = 0
    db.commit()
    return {"message": "質問を削除しました"}
