"""音声分析サービス — 語速・沈黙・敬語"""

import re
from typing import Optional

# フィラーの定義
FILLER_WORDS = {
    "えー": "えー",
    "えっと": "えっと",
    "あのー": "あのー",
    "そのー": "そのー",
    "まあ": "まあ",
    "なんか": "なんか",
    "つまり": "つまり",
    "いわゆる": "いわゆる",
    "とりあえず": "とりあえず",
    "やっぱり": "やっぱり",
}

# 敬語パターン（丁寧語・尊敬語・謙譲語）
KEIGO_PATTERNS = {
    "polite": [
        r"です", r"ます", r"でした", r"ました", r"でしょう",
        r"ください", r"ござい", r"いただき", r"申し",
    ],
    "respect": [
        r"なさ", r"おっしゃ", r"いらっしゃ", r"ご覧",
        r"お召し", r"お越し", r"くださ", r"召し上が",
    ],
    "humble": [
        r"いたし", r"申し上げ", r"承り", r"参り",
        r"お目にかか", r"拝見", r"拝聴",
    ],
}

# タメ口（敬語不使用）のパターン
CASUAL_PATTERNS = [
    r"だよね", r"だと思う", r"なんですよ", r"んだよ",
    r"してる", r"してた", r"じゃない", r"だろう",
    r"したい", r"思う", r"思って", r"言って",
]


class VoiceAnalysisService:
    """音声分析"""

    @staticmethod
    def analyze_speed(text: str, duration_seconds: float) -> dict:
        """語速分析"""
        if duration_seconds <= 0 or not text:
            return {"chars_per_min": 0, "judgment": "測定不能", "optimal": False}

        chars = len(text.replace(" ", "").replace("　", ""))
        cpm = chars / (duration_seconds / 60)

        # 日本語の理想的な話速: 毎分300〜400文字
        if cpm < 200:
            judgment = "やや遅い（落ち着きすぎ）"
            optimal = False
        elif cpm < 300:
            judgment = "ややゆっくり（面接向き）"
            optimal = True
        elif cpm < 400:
            judgment = "適切な速度（面接向き）"
            optimal = True
        elif cpm < 500:
            judgment = "やや早い（注意）"
            optimal = False
        else:
            judgment = "早すぎる（改善推奨）"
            optimal = False

        return {
            "chars_per_min": round(cpm, 1),
            "chars": chars,
            "duration_sec": round(duration_seconds, 1),
            "judgment": judgment,
            "optimal": optimal,
        }

    @staticmethod
    def analyze_fillers(text: str) -> dict:
        """フィラー分析"""
        if not text:
            return {"fillers": {}, "total": 0, "frequency": 0}

        found = {}
        total = 0
        for word, label in FILLER_WORDS.items():
            count = text.count(word)
            if count > 0:
                found[label] = count
                total += count

        # よくある言い間違い・重複
        stutter = len(re.findall(r"([、\s]|^)(.)\2+[、\s]", text))

        return {
            "fillers": found,
            "total": total,
            "stutter_count": stutter,
            "frequency_per_100chars": round(total / len(text) * 100, 1) if text else 0,
        }

    @staticmethod
    def analyze_keigo(text: str) -> dict:
        """敬語分析"""
        if not text:
            return {"score": 100, "issues": [], "suggestions": []}

        issues = []
        suggestions = []

        # 敬語使用パターン検出
        polite_count = sum(1 for p in KEIGO_PATTERNS["polite"] if re.search(p, text))
        respect_count = sum(1 for p in KEIGO_PATTERNS["respect"] if re.search(p, text))
        humble_count = sum(1 for p in KEIGO_PATTERNS["humble"] if re.search(p, text))
        casual_count = sum(1 for p in CASUAL_PATTERNS if re.search(p, text))

        keigo_total = polite_count + respect_count + humble_count

        if casual_count > 2 and keigo_total < casual_count:
            issues.append("タメ口が多い")
            suggestions.append("「〜だと思う」→「〜と考えます」")
            suggestions.append("「〜してる」→「〜しております」")

        if polite_count == 0:
            issues.append("「です・ます」調が使われていない")
            suggestions.append("基本は「です・ます」調を徹底")

        if respect_count == 0 and humble_count == 0:
            issues.append("尊敬語・謙譲語が見られない")
            suggestions.append("目上の人には尊敬語・謙譲語を使う")

        # スコア計算
        score = 100
        score -= casual_count * 5
        if polite_count == 0:
            score -= 20
        if respect_count == 0:
            score -= 10
        score = max(0, score)

        return {
            "score": score,
            "issues": issues,
            "suggestions": list(set(suggestions)),
            "details": {
                "polite_count": polite_count,
                "respect_count": respect_count,
                "humble_count": humble_count,
                "casual_count": casual_count,
            },
        }

    @staticmethod
    def analyze_all(text: str, duration_seconds: float) -> dict:
        """全分析を一括実行"""
        return {
            "speed": VoiceAnalysisService.analyze_speed(text, duration_seconds),
            "fillers": VoiceAnalysisService.analyze_fillers(text),
            "keigo": VoiceAnalysisService.analyze_keigo(text),
        }
