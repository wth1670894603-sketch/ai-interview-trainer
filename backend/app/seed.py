"""初期質問データのシード"""

from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .models.question import Question, QuestionCategory, DifficultyLevel


SAMPLE_QUESTIONS = [
    # === 自己PR ===
    {
        "category": QuestionCategory.SELF_PR,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "自己PRをお願いします。あなたの強みと、それを活かした具体的なエピソードを教えてください。",
        "purpose": "応募者の強みと、その根拠となる実体験を確認",
        "tips": "抽象的ではなく、具体的なエピソードと数字で裏付ける。PREP法を意識。",
        "expected_duration_seconds": 90,
    },
    {
        "category": QuestionCategory.SELF_PR,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "あなたの強みを発揮できた最も印象的な経験は何ですか？ その結果、周りにどのような影響を与えましたか？",
        "purpose": "強みの実践的な活用と周囲への波及効果を確認",
        "tips": "個人の成果だけでなく、チームや組織への貢献も含めると良い。",
        "expected_duration_seconds": 90,
    },
    {
        "category": QuestionCategory.SELF_PR,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "周囲からどのような人だと言われることが多いですか？ それはなぜだと思いますか？ 自己分析と他者評価にギャップはありますか？",
        "purpose": "自己認識と他者評価の一致度、自己分析力を見る",
        "tips": "複数の人からのフィードバックを挙げると説得力が増す。ギャップを正直に話すと好印象。",
        "expected_duration_seconds": 90,
    },

    # === ガクチカ ===
    {
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "学生時代に最も力を入れたことは何ですか？ なぜそれに取り組もうと思ったのですか？",
        "purpose": "主体性と熱中した経験の有無を確認",
        "tips": "「結果」だけでなく「なぜそれに取り組んだか」の動機を明確に。",
        "expected_duration_seconds": 120,
    },
    {
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "学生時代に力を入れた活動において、直面した最大の困難とその乗り越え方を教えてください。",
        "purpose": "課題解決能力と粘り強さを確認",
        "tips": "困難の具体的な内容 → どう分析したか → どう行動したか → 結果、の流れで。",
        "expected_duration_seconds": 120,
    },
    {
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "学生時代の活動で、チームメンバーと意見が対立した経験はありますか？ どのように解決しましたか？",
        "purpose": "協調性とコンフリクト解決能力を確認",
        "tips": "自分の主張だけでなく、相手の立場を理解しようとしたプロセスも含めると良い。",
        "expected_duration_seconds": 120,
    },

    # === 志望動機 ===
    {
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "当社を志望した理由を教えてください。",
        "purpose": "志望度の高さと企業理解度を確認",
        "tips": "「他社ではなく自社でなければならない理由」を含める。企業研究の深さが見られる。",
        "expected_duration_seconds": 90,
    },
    {
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "当社の事業やサービスに共感した点を具体的に教えてください。あなたの経験とどう結びつきますか？",
        "purpose": "企業理解の深さと自身との接点を確認",
        "tips": "企業の具体的な事業内容やニュースに触れ、自分の経験と結びつける。",
        "expected_duration_seconds": 90,
    },
    {
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "当社が直面している業界の課題は何だと思いますか？ その中で、あなたが貢献できることは何ですか？",
        "purpose": "業界理解、課題認識、将来展望を確認",
        "tips": "表面的な知識ではなく、自分の意見や仮説を持って答えると評価が高い。",
        "expected_duration_seconds": 120,
    },

    # === 短所 ===
    {
        "category": QuestionCategory.WEAKNESS,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "あなたの弱みを教えてください。また、それをどのように克服しようとしていますか？",
        "purpose": "自己理解と改善努力を確認",
        "tips": "弱みを正直に話した上で、改善策を具体的に述べる。単なる「努力します」は避ける。",
        "expected_duration_seconds": 60,
    },

    # === 将来像 ===
    {
        "category": QuestionCategory.FUTURE,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "5年後、10年後、あなたはどのようなキャリアを築いていたいですか？",
        "purpose": "長期的なビジョンと入社後のイメージを確認",
        "tips": "会社の中でどう成長したいか、具体的なイメージを持って話す。",
        "expected_duration_seconds": 90,
    },

    # === 逆質問 ===
    {
        "category": QuestionCategory.REVERSE_QUESTION,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "最後に、何か質問はありますか？",
        "purpose": "志望度の高さと関心の方向性を確認",
        "tips": "給与や休日などの待遇面だけでなく、仕事内容や成長機会に関する質問が好まれる。",
        "expected_duration_seconds": 60,
    },
    {
        "category": QuestionCategory.REVERSE_QUESTION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "入社後にギャップを感じた点はありますか？",
        "purpose": "現実的な視点とリサーチ力を確認",
        "tips": "調べた上での質問かどうかが見られている。OB・OG訪問で得た情報を基にすると良い。",
        "expected_duration_seconds": 60,
    },

    # === 一般 ===
    {
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "あなたの学生生活を一言で表すと何ですか？ その理由も教えてください。",
        "purpose": "自己認識と表現力を確認",
        "tips": "一言でまとめることで、自分の学生生活を本質的に捉えているかが見られる。",
        "expected_duration_seconds": 60,
    },
    {
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "最近気になっているニュースや社会問題はありますか？ それについてどう思いますか？",
        "purpose": "社会への関心度と自分の考えを持っているかを確認",
        "tips": "時事問題に関心を持ち、自分の意見を述べられることが重要。業界に関連するテーマがベスト。",
        "expected_duration_seconds": 90,
    },
]


def seed_database():
    """DBが空の場合にサンプル質問を投入"""
    init_db()

    db = SessionLocal()
    try:
        existing = db.query(Question).count()
        if existing > 0:
            print(f"既に{existing}件の質問があります。シードをスキップします。")
            return

        for i, q_data in enumerate(SAMPLE_QUESTIONS):
            q = Question(
                order_index=i,
                **{k: v for k, v in q_data.items()},
            )
            db.add(q)

        db.commit()
        print(f"{len(SAMPLE_QUESTIONS)}件の質問を追加しました。")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
