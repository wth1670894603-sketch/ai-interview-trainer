"""ユーザー情報API"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.interview import Interview
from ..models.question import Question
from ..schemas.user import UserResponse, UserUpdate, UserAdminResponse
from ..services.auth_service import get_current_user, AuthService

router = APIRouter(prefix="/api/user", tags=["ユーザー"])


# ---- 管理者用依存関係 ----
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="管理者権限が必要です")
    return current_user


# ---- 一般ユーザーAPI ----
@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """プロフィール取得"""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """プロフィール更新"""
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.delete("/me")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """アカウント削除"""
    current_user.is_active = False
    db.commit()
    return {"message": "アカウントが削除されました"}


# ---- 管理者専用API ----
@router.get("/admin/users", response_model=List[UserAdminResponse])
def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """全ユーザー一覧（管理者用）"""
    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for u in users:
        interview_count = (
            db.query(func.count(Interview.id))
            .filter(Interview.user_id == u.id)
            .scalar()
        )
        result.append(UserAdminResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            display_name=u.display_name,
            university=u.university,
            grade=u.grade,
            is_active=u.is_active,
            is_admin=u.is_admin,
            interview_count=interview_count or 0,
            created_at=u.created_at,
        ))
    return result


@router.get("/admin/stats")
def get_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """システム統計（管理者用）"""
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    total_interviews = db.query(func.count(Interview.id)).scalar()
    completed_interviews = db.query(func.count(Interview.id)).filter(
        Interview.status == "completed"
    ).scalar()
    total_questions = db.query(func.count(Question.id)).scalar()

    return {
        "total_users": total_users or 0,
        "active_users": active_users or 0,
        "total_interviews": total_interviews or 0,
        "completed_interviews": completed_interviews or 0,
        "total_questions": total_questions or 0,
    }


@router.patch("/admin/users/{user_id}/toggle-admin", response_model=UserAdminResponse)
def toggle_admin(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """ユーザーの管理者権限を切り替え"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="自分自身の権限は変更できません")

    user.is_admin = not user.is_admin
    db.commit()

    interview_count = (
        db.query(func.count(Interview.id))
        .filter(Interview.user_id == user.id)
        .scalar()
    )
    return UserAdminResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        university=user.university,
        grade=user.grade,
        is_active=user.is_active,
        is_admin=user.is_admin,
        interview_count=interview_count or 0,
        created_at=user.created_at,
    )


@router.patch("/admin/users/{user_id}/deactivate", response_model=UserAdminResponse)
def deactivate_user(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """ユーザーを無効化"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="自分自身は無効化できません")

    user.is_active = not user.is_active
    db.commit()

    interview_count = (
        db.query(func.count(Interview.id))
        .filter(Interview.user_id == user.id)
        .scalar()
    )
    return UserAdminResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        display_name=user.display_name,
        university=user.university,
        grade=user.grade,
        is_active=user.is_active,
        is_admin=user.is_admin,
        interview_count=interview_count or 0,
        created_at=user.created_at,
    )
