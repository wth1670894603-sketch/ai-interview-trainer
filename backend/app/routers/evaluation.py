"""評価API — 回答の評価とフィードバック"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.interview import Interview, InterviewQuestion
from ..schemas.evaluation import (
    EvaluationResponse, BatchEvaluationResponse, AnswerEvaluationRequest,
)
from ..services.auth_service import get_current_user
from ..services.evaluation_service import EvaluationService

router = APIRouter(prefix="/api/evaluations", tags=["評価"])


@router.post("/questions/{question_id}", response_model=EvaluationResponse)
async def evaluate_answer(
    question_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """個別回答を評価"""
    # 質問の所有権チェック
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="質問が見つかりません")

    interview = db.query(Interview).filter(
        Interview.id == question.interview_id,
        Interview.user_id == current_user.id,
    ).first()
    if not interview:
        raise HTTPException(status_code=403, detail="この質問へのアクセス権がありません")

    if not question.answer_text:
        raise HTTPException(status_code=400, detail="回答がまだ提出されていません")

    # 既存の評価があるかチェック
    existing = db.query(type(question).evaluation).filter(
        type(question).evaluation.has(interview_question_id=question_id)
    ).scalar()
    if existing:
        return EvaluationResponse.model_validate(existing)

    service = EvaluationService(db)
    evaluation = await service.evaluate_answer(question, interview,
                                                is_japanese=current_user.is_japanese)
    return EvaluationResponse.model_validate(evaluation)


@router.post("/interviews/{interview_id}/complete", response_model=BatchEvaluationResponse)
async def complete_interview_evaluation(
    interview_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """面接完了時の一括評価"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id,
    ).first()
    if not interview:
        raise HTTPException(status_code=404, detail="面接が見つかりません")

    questions = (
        db.query(InterviewQuestion)
        .filter(InterviewQuestion.interview_id == interview_id)
        .order_by(InterviewQuestion.order_index)
        .all()
    )

    if not questions:
        raise HTTPException(status_code=400, detail="質問がありません")

    service = EvaluationService(db)
    evaluations = []

    for q in questions:
        if not q.answer_text:
            continue

        # 既存の評価があれば再利用
        existing = service.get_evaluation_for_question(q.id)
        if existing:
            evaluations.append(existing)
        else:
            eval_result = await service.evaluate_answer(q, interview)
            evaluations.append(eval_result)

    if not evaluations:
        raise HTTPException(status_code=400, detail="評価できる回答がありません")

    # 面接のスコアを更新
    interview = service.update_interview_scores(interview_id)

    return BatchEvaluationResponse(
        overall_score=interview.overall_score or 0.0,
        content_score=interview.content_score or 0.0,
        structure_score=interview.structure_score or 0.0,
        language_score=interview.language_score or 0.0,
        passion_score=interview.passion_score or 0.0,
        manners_score=interview.manners_score or 0.0,
        feedback_summary=interview.feedback_summary or "",
        improvement_tips=interview.improvement_tips or "",
        question_evaluations=[EvaluationResponse.model_validate(e) for e in evaluations],
    )


@router.get("/questions/{question_id}", response_model=EvaluationResponse)
def get_evaluation(
    question_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """個別評価結果を取得"""
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="質問が見つかりません")

    interview = db.query(Interview).filter(
        Interview.id == question.interview_id,
        Interview.user_id == current_user.id,
    ).first()
    if not interview:
        raise HTTPException(status_code=403, detail="アクセス権がありません")

    evaluation = db.query(type(question).evaluation).filter(
        type(question).evaluation.has(interview_question_id=question_id)
    ).scalar()
    if not evaluation:
        raise HTTPException(status_code=404, detail="評価がまだありません")

    return EvaluationResponse.model_validate(evaluation)
