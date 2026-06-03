"""ES（エントリーシート）API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.es import ES, ESCategory
from ..schemas.es import ESCreate, ESResponse, ESGenerateResponse
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/es", tags=["ES（エントリーシート）"])


@router.post("", response_model=ESResponse)
def create_es(
    data: ESCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ESを登録"""
    es = ES(
        user_id=current_user.id,
        title=data.title,
        category=ESCategory(data.category),
        content=data.content,
        target_company=data.target_company,
        target_position=data.target_position,
    )
    db.add(es)
    db.commit()
    db.refresh(es)
    return ESResponse.model_validate(es)


@router.get("", response_model=List[ESResponse])
def list_es(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """自分のES一覧"""
    entries = (
        db.query(ES)
        .filter(ES.user_id == current_user.id)
        .order_by(ES.created_at.desc())
        .all()
    )
    return [ESResponse.model_validate(e) for e in entries]


@router.delete("/{es_id}")
def delete_es(
    es_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ESを削除"""
    es = db.query(ES).filter(ES.id == es_id, ES.user_id == current_user.id).first()
    if not es:
        raise HTTPException(status_code=404, detail="ESが見つかりません")
    db.delete(es)
    db.commit()
    return {"message": "削除しました"}


@router.post("/{es_id}/generate", response_model=ESGenerateResponse)
async def generate_questions(
    es_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ESから面接質問を生成"""
    es = db.query(ES).filter(ES.id == es_id, ES.user_id == current_user.id).first()
    if not es:
        raise HTTPException(status_code=404, detail="ESが見つかりません")

    # LLMで質問生成
    from ..services.llm_service import LLMService

    prompt = f"""あなたは面接官です。以下のES（エントリーシート）を読んで、面接で質問すべきことを3つ考えてください。

## ESカテゴリ
{es.category.value}

## ES本文
{es.content}

"""

    if es.target_company:
        prompt += f"## 志望企業\n{es.target_company}\n"
    if es.target_position:
        prompt += f"## 志望職種\n{es.target_position}\n"

    prompt += """
以下のJSON形式で出力してください：
{
  "questions": [
    {
      "question_text": "質問文",
      "purpose": "この質問の意図",
      "tips": "回答のポイント"
    }
  ]
}
"""

    try:
        llm = LLMService()
        result = await llm._call_openai(prompt)

        questions = result.get("questions", [])
        return ESGenerateResponse(
            es_id=es_id,
            questions=[
                {
                    "question_text": q.get("question_text", ""),
                    "purpose": q.get("purpose", ""),
                    "tips": q.get("tips", ""),
                }
                for q in questions[:5]
            ],
        )
    except Exception:
        # フォールバック: モック質問
        return ESGenerateResponse(
            es_id=es_id,
            questions=[
                {
                    "question_text": f"あなたのESにある「{es.title}」について詳しく教えてください。",
                    "purpose": "ESの内容を掘り下げる",
                    "tips": "具体的なエピソードを交えて答える",
                },
                {
                    "question_text": "なぜその活動に取り組もうと思ったのですか？",
                    "purpose": "動機を確認",
                    "tips": "自分の言葉で理由を説明する",
                },
                {
                    "question_text": "その経験から何を学び、どう成長しましたか？",
                    "purpose": "学びと成長を確認",
                    "tips": "入社後にどう活かせるかまで言及すると良い",
                },
            ],
        )
