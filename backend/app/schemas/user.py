"""ユーザー関連スキーマ"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """新規ユーザー登録"""
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=100, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6)
    display_name: str = ""
    is_japanese: bool = True
    university: str = ""
    grade: str = ""
    target_industry: str = ""


class UserLogin(BaseModel):
    """ログイン"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """プロフィール更新"""
    display_name: Optional[str] = None
    is_japanese: Optional[bool] = None
    university: Optional[str] = None
    grade: Optional[str] = None
    target_industry: Optional[str] = None


class UserResponse(BaseModel):
    """ユーザー情報レスポンス"""
    id: str
    email: str
    username: str
    display_name: str
    is_japanese: bool
    university: str
    grade: str
    target_industry: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWTトークンレスポンス"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    class Config:
        from_attributes = True


class UserAdminResponse(BaseModel):
    """管理者向けユーザー一覧"""
    id: str
    email: str
    username: str
    display_name: str
    university: str
    grade: str
    is_active: bool
    is_admin: bool
    interview_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
