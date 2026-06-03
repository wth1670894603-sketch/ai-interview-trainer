"""評価サービス — LLMを使った回答評価と集計"""

import time
from typing import Optional

from sqlalchemy.orm import Session

from ..models.interview import Interview, InterviewQuestion
from ..models.evaluation import Evaluation, EvaluationDetail
from ..services.llm_service import LLMService


class EvaluationService:
    """回答評価のビジネスロジック"""

    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()

    async def evaluate_answer(
        self,
        question: InterviewQuestion,
        interview: Interview,
        is_japanese: bool = True,
    ) -> Evaluation:
        """個別の回答を評価"""
        start_time = time.time()

        # LLMで評価
        result = await self.llm.evaluate_answer(
            question=question.question_text,
            answer=question.answer_text or "",
            category=question.question_category,
            company=interview.target_company,
            industry=interview.target_industry,
        )

        duration_ms = (time.time() - start_time) * 1000

        # 評価をDBに保存
        evaluation = Evaluation(
            interview_question_id=question.id,
            overall_score=result.get("overall_score", 0),
            content_score=result.get("content", {}).get("score", 0),
            structure_score=result.get("structure", {}).get("score", 0),
            language_score=result.get("language", {}).get("score", 0),
            passion_score=result.get("passion", {}).get("score", 0),
            manners_score=result.get("manners", {}).get("score", 0),
            content_feedback=result.get("content", {}).get("feedback", ""),
            structure_feedback=result.get("structure", {}).get("feedback", ""),
            language_feedback=result.get("language", {}).get("feedback", ""),
            improvement_suggestions=result.get("improvement_suggestions", ""),
            strengths=result.get("content", {}).get("strengths", []),
            weaknesses=result.get("content", {}).get("weaknesses", []),
            suggested_answer_points=result.get("suggested_answer_points", []),
            model_used="llm",
            evaluation_duration_ms=duration_ms,
        )

        self.db.add(evaluation)
        self.db.flush()  # evaluation.id を確定

        detail = EvaluationDetail(
            evaluation_id=evaluation.id,
            raw_response=result,
        )
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(evaluation)

        return evaluation

    def update_interview_scores(self, interview_id: str) -> Optional[Interview]:
        """面接の全回答評価を集計して全体スコアを計算"""
        interview = self.db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            return None

        evaluations = (
            self.db.query(Evaluation)
            .join(InterviewQuestion)
            .filter(InterviewQuestion.interview_id == interview_id)
            .all()
        )

        if not evaluations:
            return interview

        n = len(evaluations)
        interview.content_score = sum(e.content_score for e in evaluations) / n
        interview.structure_score = sum(e.structure_score for e in evaluations) / n
        interview.language_score = sum(e.language_score for e in evaluations) / n
        interview.passion_score = sum(e.passion_score for e in evaluations) / n
        interview.manners_score = sum(e.manners_score for e in evaluations) / n
        interview.overall_score = sum(e.overall_score for e in evaluations) / n

        # 総評と改善点の生成
        weak_areas = []
        scores = {
            "内容": interview.content_score,
            "構成": interview.structure_score,
            "言語": interview.language_score,
            "熱意": interview.passion_score,
            "マナー": interview.manners_score,
        }
        for area, score in sorted(scores.items(), key=lambda x: x[1]):
            if score < 70:
                weak_areas.append(area)

        if weak_areas:
            interview.feedback_summary = (
                f"全{len(evaluations)}問の回答、お疲れ様でした。"
                f"総合スコアは{interview.overall_score:.0f}点です。"
                f"特に「{'」「'.join(weak_areas)}」の分野で改善の余地があります。"
                f"各質問の詳細フィードバックを確認し、次の練習に活かしてください。"
            )
        else:
            interview.feedback_summary = (
                f"全{len(evaluations)}問の回答、素晴らしい出来でした。"
                f"総合スコアは{interview.overall_score:.0f}点です。"
                f"各分野でバランスの取れた回答ができています。"
                f"この調子で本番に臨んでください！"
            )

        # 改善点の集約
        all_tips = []
        for e in evaluations:
            if e.improvement_suggestions:
                all_tips.append(e.improvement_suggestions)

        interview.improvement_tips = "\n".join(all_tips[:3]) if all_tips else ""

        self.db.commit()
        self.db.refresh(interview)
        return interview

    def get_evaluation_for_question(
        self, question_id: str
    ) -> Optional[Evaluation]:
        """質問に対する評価を取得"""
        return (
            self.db.query(Evaluation)
            .filter(Evaluation.interview_question_id == question_id)
            .first()
        )
