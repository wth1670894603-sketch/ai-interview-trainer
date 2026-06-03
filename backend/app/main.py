"""AI面接トレーナー — FastAPI エントリポイント"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routers import (
    auth_router,
    interview_router,
    evaluation_router,
    user_router,
    admin_questions_router,
    setup_router,
    es_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーション起動・終了処理"""
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="日本大学生向けAI面接練習プラットフォーム",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(interview_router)
app.include_router(evaluation_router)
app.include_router(admin_questions_router)
app.include_router(setup_router)
app.include_router(es_router)


@app.get("/api/health")
def health_check():
    """ヘルスチェック"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": "0.1.0",
    }
