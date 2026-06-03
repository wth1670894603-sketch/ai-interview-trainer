"""認証API — 登録・ログイン"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["認証"])


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """新規ユーザー登録"""
    user, token = AuthService.register_user(db, user_data)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """ログイン"""
    user, token = AuthService.login_user(db, login_data.email, login_data.password)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )
