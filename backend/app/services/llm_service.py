"""LLM API 統合サービス — OpenAI / Claude 対応"""

import json
import time
from typing import Optional

import httpx

from ..config import settings


class LLMService:
    """LLM API 呼び出しの抽象レイヤー"""

    DEFAULT_SYSTEM_PROMPT = """あなたは日本の面接官です。
大学生の面接回答を評価し、建設的なフィードバックを提供してください。
評価は厳しすぎず、甘すぎず、具体的に改善点を指摘してください。

評価基準：
- 内容 (0-100): 回答の具体性、論理性、説得力
- 構成 (0-100): PREP法などの構造、結論ファースト
- 言語 (0-100): 敬語、文法、語彙、表現の適切さ
- 熱意 (0-100): 志望動機の一貫性、熱意の伝わり方
- マナー (0-100): 言葉遣い、時間配分、面接マナー

必ずJSON形式で返答してください。"""

    @staticmethod
    def _build_evaluation_prompt(question: str, answer: str, category: str = "",
                                  company: str = "", industry: str = "") -> str:
        prompt = f"""以下の面接の回答を評価してください。

## 質問
{question}

## 回答
{answer}

"""
        if category:
            prompt += f"## 質問カテゴリ\n{category}\n"
        if company:
            prompt += f"## 志望企業\n{company}\n"
        if industry:
            prompt += f"## 志望業界\n{industry}\n"

        prompt += """
## 評価出力（JSON）
{
  "overall_score": <0-100>,
  "content": {
    "score": <0-100>,
    "feedback": "内容の評価",
    "strengths": ["強み1", "強み2"],
    "weaknesses": ["弱み1"]
  },
  "structure": {
    "score": <0-100>,
    "feedback": "構成の評価"
  },
  "language": {
    "score": <0-100>,
    "feedback": "日本語の評価",
    "improvements": ["改善点1"]
  },
  "passion": {
    "score": <0-100>,
    "feedback": "熱意の評価"
  },
  "manners": {
    "score": <0-100>,
    "feedback": "マナーの評価"
  },
  "suggested_answer_points": ["模範回答のポイント1", "ポイント2"],
  "improvement_suggestions": "全体的な改善提案"
}"""

        return prompt

    @staticmethod
    async def evaluate_answer(
        question: str,
        answer: str,
        category: str = "",
        company: str = "",
        industry: str = "",
    ) -> dict:
        """回答をLLMで評価"""
        prompt = LLMService._build_evaluation_prompt(
            question, answer, category, company, industry
        )

        # OpenAI 優先、なければ Claude
        openai_key = settings.openai_api_key or ""
        anthropic_key = settings.anthropic_api_key or ""

        if openai_key and not openai_key.startswith("sk-your-"):
            return await LLMService._call_openai(prompt)
        elif anthropic_key and not anthropic_key.startswith("sk-ant-your-"):
            return await LLMService._call_anthropic(prompt)
        else:
            # APIキーがない or プレースホルダーの場合はモック評価（開発用）
            return LLMService._mock_evaluation(question, answer)

    @staticmethod
    async def _call_openai(system_prompt: str, user_prompt: str = "") -> dict:
        """OpenAI API呼び出し"""
        if not user_prompt:
            # evaluate_answer の場合は system_prompt に全部入っている
            messages = [
                {"role": "system", "content": LLMService.DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": system_prompt},
            ]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.openai_model,
                    "messages": messages,
                    "temperature": 0.7,
                    "response_format": {"type": "json_object"},
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)

    @staticmethod
    async def _call_anthropic(prompt: str) -> dict:
        """Claude API呼び出し"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.anthropic_model,
                    "max_tokens": 2000,
                    "system": LLMService.DEFAULT_SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["content"][0]["text"]

            # JSON を抽出（Claudeは時々余計な文章を付ける）
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])
            return json.loads(content)

    @staticmethod
    def _mock_evaluation(question: str, answer: str) -> dict:
        """開発用モック評価"""
        import random

        base_score = random.uniform(55, 85)

        return {
            "overall_score": round(base_score, 1),
            "content": {
                "score": round(base_score + random.uniform(-5, 5), 1),
                "feedback": "具体的なエピソードが含まれており、説得力があります。"
                           "さらに数字を用いるとより具体性が増します。",
                "strengths": ["論理的な構成", "前向きな姿勢"],
                "weaknesses": ["もう少し具体的な事例が欲しい"],
            },
            "structure": {
                "score": round(base_score + random.uniform(-10, 5), 1),
                "feedback": "結論ファーストの構成が取れています。"
                           "PREP法を意識するとさらに良くなります。",
            },
            "language": {
                "score": round(base_score + random.uniform(-5, 10), 1),
                "feedback": "丁寧な言葉遣いができています。"
                           "「〜と思います」がやや多いので、"
                           "「〜と考えます」に置き換えるとより印象が良くなります。",
                "improvements": ["「思います」→「考えます」", "もう少し簡潔に"],
            },
            "passion": {
                "score": round(base_score + random.uniform(-5, 10), 1),
                "feedback": "志望動機に一貫性があり、熱意が伝わります。",
            },
            "manners": {
                "score": round(base_score + random.uniform(-5, 10), 1),
                "feedback": "適切な時間配分です。"
                           "もう少しアイコンタクト（カメラ目線）を意識しましょう。",
            },
            "suggested_answer_points": [
                "結論を最初に述べる",
                "具体的な数字を入れる",
                "志望動機と一貫性を持たせる",
            ],
            "improvement_suggestions": "全体的によくまとまっています。"
                                      "さらに具体性を増すことで、より印象的な回答になります。"
                                      "また、時間配分にも注意しましょう。",
        }
