from .auth import router as auth_router
from .interview import router as interview_router
from .evaluation import router as evaluation_router
from .user import router as user_router
from .admin_questions import router as admin_questions_router
from .setup import router as setup_router

__all__ = [
    "auth_router",
    "interview_router",
    "evaluation_router",
    "user_router",
    "admin_questions_router",
    "setup_router",
]
