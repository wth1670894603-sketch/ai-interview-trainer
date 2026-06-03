"""管理者アカウントを作成"""

from .database import SessionLocal, init_db
from .models.user import User
from .services.auth_service import AuthService


def create_admin():
    """管理者アカウントを作成（既存ならスキップ）"""
    init_db()

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.is_admin == True).first()
        if admin:
            print(f"管理者アカウントは既に存在します: {admin.email}")
            return

        # デフォルト管理者
        admin = User(
            email="admin@interview-trainer.app",
            username="admin",
            hashed_password=AuthService.hash_password("admin123"),
            display_name="管理者",
            is_japanese=True,
            is_active=True,
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        print("✅ 管理者アカウントを作成しました")
        print(f"   メール: admin@interview-trainer.app")
        print(f"   パスワード: admin123")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
