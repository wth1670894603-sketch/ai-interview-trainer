"""面接セッションAPI"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.interview import Interview, InterviewQuestion, InterviewStatus
from ..schemas.interview import (
    InterviewCreate, InterviewResponse, InterviewStartResponse,
    InterviewQuestionResponse, InterviewQuestionAnswer,
)
from ..services.auth_service import get_current_user
from ..services.interview_engine import InterviewEngine

router = APIRouter(prefix="/api/interviews", tags=["面接"])


@router.post("", response_model=InterviewResponse)
def create_interview(
    data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """新規面接セッションを作成"""
    engine = InterviewEngine(db)
    interview = engine.create_interview(current_user.id, data)
    return InterviewResponse.model_validate(interview)


@router.get("", response_model=list[InterviewResponse])
def list_interviews(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """面接履歴一覧"""
    engine = InterviewEngine(db)
    interviews = engine.get_interviews_for_user(current_user.id, limit, offset)
    return [InterviewResponse.model_validate(i) for i in interviews]


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """面接詳細を取得"""
    engine = InterviewEngine(db)
    interview = engine.get_interview_detail(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="面接が見つかりません")
    return InterviewResponse.model_validate(interview)


@router.post("/{interview_id}/start", response_model=InterviewStartResponse)
def start_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """面接を開始"""
    engine = InterviewEngine(db)
    interview = engine.get_interview_detail(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="面接が見つかりません")

    if interview.status != InterviewStatus.PENDING:
        raise HTTPException(status_code=400, detail="この面接は既に開始されています")

    first_q = engine.start_interview(interview_id)
    if not first_q:
        raise HTTPException(status_code=400, detail="質問が設定されていません")

    return InterviewStartResponse(
        interview_id=interview_id,
        question=InterviewQuestionResponse.model_validate(first_q),
        total_questions=interview.question_count,
    )


@router.post("/{interview_id}/questions/{order}/answer", response_model=InterviewQuestionResponse)
def submit_answer(
    interview_id: str,
    order: int,
    answer: InterviewQuestionAnswer,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """回答を提出"""
    engine = InterviewEngine(db)
    interview = engine.get_interview_detail(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="面接が見つかりません")

    q = engine.submit_answer(
        interview_id=interview_id,
        question_order=order,
        answer_text=answer.answer_text,
        duration=answer.answer_duration_seconds,
    )
    if not q:
        raise HTTPException(status_code=404, detail="質問が見つかりません")

    return InterviewQuestionResponse.model_validate(q)


@router.get("/{interview_id}/next/{current_order}", response_model=InterviewQuestionResponse)
def get_next_question(
    interview_id: str,
    current_order: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """次の質問を取得"""
    engine = InterviewEngine(db)
    interview = engine.get_interview_detail(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="面接が見つかりません")

    next_q = engine.get_next_question(interview_id, current_order)
    if not next_q:
        raise HTTPException(status_code=404, detail="これが最後の質問です")

    return InterviewQuestionResponse.model_validate(next_q)


@router.post("/{interview_id}/complete", response_model=InterviewResponse)
def complete_interview(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """面接を完了"""
    engine = InterviewEngine(db)
    interview = engine.get_interview_detail(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="面接が見つかりません")

    engine.complete_interview(interview_id)
    db.refresh(interview)
    return InterviewResponse.model_validate(interview)
