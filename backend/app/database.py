"""データベース接続設定"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings

db_url = settings.effective_db_url

# SQLite の場合はデータディレクトリ作成
if "sqlite" in db_url:
    db_path = db_url.replace("sqlite:///", "")
    db_dir = os.path.dirname(os.path.abspath(db_path))
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """依存性注入用のDBセッション"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初回テーブル作成"""
    from .models import user, interview, question, evaluation  # noqa
    Base.metadata.create_all(bind=engine)
