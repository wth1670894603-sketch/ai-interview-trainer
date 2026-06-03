"""面接エンジン — 質問生成・セッション管理"""

import random
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from ..models.interview import (
    Interview, InterviewQuestion, InterviewStatus, InterviewType,
)
from ..models.question import Question, QuestionCategory
from ..schemas.interview import InterviewCreate


class InterviewEngine:
    """面接セッションの作成・進行管理"""

    # 質問カテゴリの配分（個人面接の場合）
    DEFAULT_QUESTION_MIX = [
        QuestionCategory.SELF_PR,
        QuestionCategory.GAKUCHIKA,
        QuestionCategory.MOTIVATION,
        QuestionCategory.WEAKNESS,
        QuestionCategory.FUTURE,
        QuestionCategory.GENERAL,
    ]

    def __init__(self, db: Session):
        self.db = db

    def create_interview(self, user_id: str, data: InterviewCreate) -> Interview:
        """面接セッションを作成し、質問を割り当てる"""
        interview = Interview(
            user_id=user_id,
            interview_type=InterviewType(data.interview_type),
            status=InterviewStatus.PENDING,
            target_company=data.target_company,
            target_industry=data.target_industry,
            target_position=data.target_position,
            major=data.major,
            university=data.university,
            duration_minutes=data.duration_minutes,
            question_count=data.question_count,
        )
        self.db.add(interview)
        self.db.flush()

        # 質問の割り当て
        questions = self._select_questions(data, interview.id)
        for q in questions:
            self.db.add(q)

        self.db.commit()
        self.db.refresh(interview)
        return interview

    def _select_questions(self, data: InterviewCreate, interview_id: str) -> list[InterviewQuestion]:
        """面接タイプに応じて質問を選択（企業別質問を優先）"""
        # DBからアクティブな質問を取得
        db_questions: list[Question] = (
            self.db.query(Question)
            .filter(Question.is_active == 1)
            .all()
        )

        # 企業固有質問を優先
        company_questions = [
            q for q in db_questions
            if data.target_company and q.target_company
            and q.target_company.lower() in data.target_company.lower()
        ]
        if company_questions:
            db_questions = company_questions + [
                q for q in db_questions if q not in company_questions
            ]

        # 職種固有質問を優先（企業質問より低い優先度）
        position_questions = [
            q for q in db_questions
            if data.target_position and q.target_position
            and q.target_position.lower() in data.target_position.lower()
        ]
        if position_questions:
            for pq in position_questions:
                if pq in db_questions:
                    db_questions.remove(pq)
            db_questions = position_questions + company_questions + [
                q for q in db_questions if q not in position_questions
            ]

        if not db_questions:
            # DBに質問がない場合はデフォルト質問を生成
            return self._generate_default_questions(interview_id, data)

        # カテゴリ配分を決定
        if data.interview_type == "gd":
            categories = [QuestionCategory.GD, QuestionCategory.GENERAL]
        elif data.interview_type == "case":
            categories = [QuestionCategory.CASE, QuestionCategory.GENERAL]
        elif data.interview_type == "reverse":
            categories = [QuestionCategory.REVERSE_QUESTION]
        else:
            categories = self.DEFAULT_QUESTION_MIX

        # カテゴリから均等に選択
        selected = []
        per_category = max(1, data.question_count // len(categories))

        for cat in categories:
            pool = [q for q in db_questions if q.category == cat]
            if pool:
                chosen = random.sample(pool, min(per_category, len(pool)))
                for q in chosen:
                    selected.append(InterviewQuestion(
                        interview_id=interview_id,
                        question_id=q.id,
                        question_text=q.text_ja,
                        question_category=cat.value,
                        order_index=len(selected),
                    ))

        # 足りない分をランダム補充
        while len(selected) < data.question_count and db_questions:
            q = random.choice(db_questions)
            selected.append(InterviewQuestion(
                interview_id=interview_id,
                question_id=q.id,
                question_text=q.text_ja,
                question_category=q.category.value,
                order_index=len(selected),
            ))

        return selected[:data.question_count]

    def _generate_default_questions(
        self, interview_id: str, data: InterviewCreate
    ) -> list[InterviewQuestion]:
        """DBに質問がない場合のフォールバック質問"""
        defaults = [
            ("自己PRをお願いします。あなたの強みと、それを活かしたエピソードを教えてください。",
             "self_pr"),
            ("学生時代に最も力を入れたことは何ですか？", "gakuchika"),
            ("当社を志望した理由を教えてください。", "motivation"),
            ("あなたの弱みと、それをどう克服しているか教えてください。", "weakness"),
            ("10年後、どのようなキャリアを築いていたいですか？", "future"),
            ("当社で挑戦したいことは何ですか？", "motivation"),
            ("学生時代に最も困難だった経験と、その乗り越え方を教えてください。",
             "gakuchika"),
        ]

        # target_company があれば志望動機をカスタマイズ
        questions = []
        for i, (text, category) in enumerate(defaults[:data.question_count]):
            q_text = text
            if data.target_company and category == "motivation":
                q_text = f"当社（{data.target_company}）を志望した理由を教えてください。"

            questions.append(InterviewQuestion(
                interview_id=interview_id,
                question_id=None,
                question_text=q_text,
                question_category=category,
                order_index=i,
            ))

        return questions

    def start_interview(self, interview_id: str) -> Optional[InterviewQuestion]:
        """面接を開始し、最初の質問を返す"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return None

        interview.status = InterviewStatus.IN_PROGRESS
        interview.started_at = datetime.now(timezone.utc)
        self.db.commit()

        return interview.questions[0] if interview.questions else None

    def get_next_question(self, interview_id: str, current_order: int) -> Optional[InterviewQuestion]:
        """次の質問を取得"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return None

        next_q = (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id,
                InterviewQuestion.order_index == current_order + 1,
            )
            .first()
        )
        return next_q

    def submit_answer(
        self,
        interview_id: str,
        question_order: int,
        answer_text: str,
        audio_path: str = "",
        duration: float = 0.0,
    ) -> Optional[InterviewQuestion]:
        """回答を保存"""
        q = (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id,
                InterviewQuestion.order_index == question_order,
            )
            .first()
        )
        if not q:
            return None

        q.answer_text = answer_text
        q.answer_audio_path = audio_path
        q.answer_duration_seconds = duration
        q.answered_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(q)
        return q

    def complete_interview(self, interview_id: str) -> bool:
        """面接を完了状態にする"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return False

        interview.status = InterviewStatus.COMPLETED
        interview.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        return True

    def get_interviews_for_user(self, user_id: str, limit: int = 20, offset: int = 0):
        """ユーザーの面接一覧"""
        return (
            self.db.query(Interview)
            .filter(Interview.user_id == user_id)
            .order_by(Interview.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_interview_detail(self, interview_id: str) -> Optional[Interview]:
        """面接詳細を取得（質問+評価を含む）"""
        return (
            self.db.query(Interview)
            .filter(Interview.id == interview_id)
            .first()
        )
