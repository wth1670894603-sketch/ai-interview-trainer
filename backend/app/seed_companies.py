"""大手企業別の面接質問シードデータ"""

from .database import SessionLocal
from .models.question import Question, QuestionCategory, DifficultyLevel


COMPANY_QUESTIONS = [
    # ======== 楽天 ========
    {
        "target_company": "楽天",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "数あるIT企業の中で、なぜ楽天を志望するのですか？「楽天主義」のどの部分に共感しましたか？",
        "purpose": "楽天の企業文化（楽天主義）への理解と共感度を確認",
        "tips": "「樂天主義」の5項目（スピード×品質、革新、改善、エンパワーメント、プロフェッショナリズム）に触れ、自分の経験と結びつける。英語力への意欲も示すと良い。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "楽天",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "楽天経済圏（Rakuten Ecosystem）の現状の課題は何だと思いますか？あなたならどう改善しますか？",
        "purpose": "楽天全体のビジネス理解と課題発見力を確認",
        "tips": "楽天の各サービス（ショッピング、銀行、カード、モバイルなど）間のシナジーやクロスユース率などの観点から自分の意見を持つ。",
        "expected_duration_seconds": 120,
    },
    {
        "target_company": "楽天",
        "category": QuestionCategory.SELF_PR,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "楽天は英語を社内公用語としています。あなたの英語力と、グローバル環境で働くことへの考えを教えてください。",
        "purpose": "英語力とグローバル志向を確認",
        "tips": "現在の英語力（TOEICなど）を正直に話し、英語での業務に前向きな姿勢を示す。将来の目標も含めると良い。",
        "expected_duration_seconds": 60,
    },
    {
        "target_company": "楽天",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "これまでに「スピード」を意識して成果を出した経験はありますか？具体的に教えてください。",
        "purpose": "楽天が重視する「スピード×品質」への適応力を確認",
        "tips": "素早く行動した結果と、その中で品質も担保したプロセスを具体的に。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "楽天",
        "category": QuestionCategory.REVERSE_QUESTION,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "楽天の社内公用語が英語であることについて、入社後のギャップを感じることはありますか？",
        "purpose": "逆質問を通じて企業理解度を見る",
        "tips": "英語に不安があっても素直に聞くのは好印象。OBOG訪問で聞いた情報をもとにすると良い。",
        "expected_duration_seconds": 60,
    },

    # ======== メルカリ ========
    {
        "target_company": "メルカリ",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "メルカリの4つのバリュー（Go Bold, All for One, Be a Pro, Move Fast）の中で、最も共感できるものは何ですか？その理由と、あなたの経験を交えて教えてください。",
        "purpose": "メルカリのカルチャーフィットを確認",
        "tips": "バリューを単に暗記するのではなく、自分の経験と結びつけて語る。「Go Bold」なら挑戦した経験、「All for One」ならチーム貢献のエピソードなど。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "メルカリ",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "メルカリのサービスについて、改善点や新機能のアイデアはありますか？",
        "purpose": "プロダクトへの深い理解と提案力を確認",
        "tips": "ユーザー視点での具体的な改善案を、なぜ必要かという根拠とともに述べる。技術的な実現性にこだわらなくて良いが、論理的な理由が必要。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "メルカリ",
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.EASY,
        "text_ja": "メルカリをファーストキャリアとして選んだ理由を教えてください。",
        "purpose": "新卒でメルカリを選ぶ理由の明確さを確認",
        "tips": "「メルカリでなければならない理由」を明確に。成長環境、ミッションへの共感、プロダクトへの愛着など。",
        "expected_duration_seconds": 60,
    },

    # ======== アクセンチュア ========
    {
        "target_company": "アクセンチュア",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "アクセンチュアは総合コンサルティングファームです。あなたはどの領域（戦略/テクノロジー/デジタル/オペレーションズ）で活躍したいですか？その理由は？",
        "purpose": "志望領域とキャリアビジョンの明確さを確認",
        "tips": "各領域の違いを理解した上で、自分の強みや興味と照らし合わせて選ぶ。領域横断的に成長したい意欲もアピールできる。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "アクセンチュア",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "チームで成果を出すために、あなたが特に意識していることは何ですか？具体的なエピソードを教えてください。",
        "purpose": "チームワークとコミュニケーション能力を確認",
        "tips": "プロジェクトにおける役割、メンバーとの調整方法、コンフリクト解決の経験などを具体的に。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "アクセンチュア",
        "category": QuestionCategory.CASE,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "あるカフェチェーンの売上を20%向上させるには、どうすれば良いですか？論理的に考えて提案してください。",
        "purpose": "ケース面接の練習。論理的思考力とフレームワーク思考を確認",
        "tips": "3C/4Pなどのフレームワークを使って構造化。客数×客単価に分解し、それぞれに施策を考える。数字の仮説を入れると説得力が増す。",
        "expected_duration_seconds": 180,
    },
    {
        "target_company": "アクセンチュア",
        "category": QuestionCategory.CASE,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "日本のコンビニエンスストアの市場規模を推定してください。",
        "purpose": "フェルミ推定の練習",
        "tips": "店舗数×1店舗あたりの売上の積で計算。仮定を明確にし、計算過程を説明する。",
        "expected_duration_seconds": 120,
    },

    # ======== 外資系コンサル汎用ケース ========
    {
        "target_industry": "コンサル",
        "category": QuestionCategory.CASE,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "日本のミネラルウォーターの年間市場規模を推定してください。",
        "purpose": "フェルミ推定の基礎力を確認",
        "tips": "人口×1人当たりの年間消費量でアプローチ。年齢別の消費量の違いも考慮できると良い。",
        "expected_duration_seconds": 120,
    },
    {
        "target_industry": "コンサル",
        "category": QuestionCategory.CASE,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "東京都民の通勤時間を減らすにはどうすれば良いですか？",
        "purpose": "抽象的な社会課題へのアプローチ力を見る",
        "tips": "問題を構造化（テレワーク推進、時差出勤、交通網改善など）し、各施策の効果と実現可能性を論じる。",
        "expected_duration_seconds": 180,
    },

    # ======== 三菱UFJ (メガバンク) ========
    {
        "target_industry": "金融",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "メガバンクの中で、なぜ当行を志望するのですか？他行との違いを踏まえて教えてください。",
        "purpose": "金融業界の理解度と企業選びの軸を確認",
        "tips": "3メガバンク（三菱UFJ、三井住友、みずほ）の違いを理解した上で、自社を選ぶ理由を具体的に。規模感、海外展開、デジタル戦略などの観点から。",
        "expected_duration_seconds": 90,
    },
    {
        "target_industry": "金融",
        "category": QuestionCategory.FUTURE,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "10年後、銀行業界はどのように変わっていると思いますか？その中で、あなたはどのような価値を提供したいですか？",
        "purpose": "業界の将来展望と自身のキャリアビジョンの一致を見る",
        "tips": "フィンテック、キャッシュレス、AI活用などのトレンドを踏まえた上で、自分がどう貢献するかを語る。",
        "expected_duration_seconds": 90,
    },

    # ======== トヨタ (メーカー) ========
    {
        "target_industry": "メーカー",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "モノづくり企業として、私たちの一番の財産は「人」です。あなたはどのような観点から、私たちの仲間になりたいと考えていますか？",
        "purpose": "製造業への理解と「人」への価値観を確認",
        "tips": "トヨタの「カイゼン」や「人材育成」に関する考え方に触れ、自分の成長意欲と結びつける。",
        "expected_duration_seconds": 90,
    },

    # ======== 電通 (広告) ========
    {
        "target_industry": "広告",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "広告業界を志望する理由を教えてください。また、その中でもなぜ当社なのですか？",
        "purpose": "広告業界への志望度と企業理解を確認",
        "tips": "広告の「社会的な影響力」と「ビジネスとしての側面」の両方を理解していることを示す。自分の経験（サークルの広報など）と結びつけると良い。",
        "expected_duration_seconds": 90,
    },

    # ======== LINE / Yahoo (IT) ========
    {
        "target_company": "LINE",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "LINEのサービスの中で、あなたが最も改善すべきだと思う機能は何ですか？理由と改善案を教えてください。",
        "purpose": "プロダクト理解と課題発見力を確認",
        "tips": "ユーザーとしての体験をベースに、具体的な改善案を提案する。技術面に詳しくなくても、ユーザー視点の提案でOK。",
        "expected_duration_seconds": 90,
    },

    # ======== Google Japan ========
    {
        "target_company": "Google",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "Googleの10の事実（Ten things we know to be true）の中で、最も共感するものを教えてください。その理由と、あなたの経験を交えて説明してください。",
        "purpose": "Googleの企業哲学への理解と共感を確認",
        "tips": "「ユーザーに焦点を合わせよ」「収入がなくてもよいことを」「速さはすべて」など、具体的な項目に触れ、自分の価値観と結びつける。",
        "expected_duration_seconds": 90,
    },
    {
        "target_company": "Google",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "これまでに、誰もやったことがないことに挑戦した経験はありますか？その結果どうなりましたか？",
        "purpose": "Googleが重視する「革新的思考」と「大胆さ」を確認",
        "tips": "失敗を恐れない姿勢と、そこからの学びを強調する。成果よりもプロセスとチャレンジ精神が評価される。",
        "expected_duration_seconds": 90,
    },

    # ======== ソニー ========
    {
        "target_company": "ソニー",
        "category": QuestionCategory.MOTIVATION,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "ソニーの事業領域（エレクトロニクス、エンタテインメント、金融）の中で、最も興味がある領域はどこですか？その理由を教えてください。",
        "purpose": "ソニーの事業理解と関心領域を確認",
        "tips": "ソニーの技術力（イメージセンサーなど）やコンテンツ事業（ゲーム・音楽・映画）など、具体的な事業に触れる。",
        "expected_duration_seconds": 90,
    },

    # ======== 職種別質問 ========
    {
        "target_position": "エンジニア",
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "これまでにプログラミングで最も困難だった課題と、その解決方法を教えてください。",
        "purpose": "エンジニアとしての課題解決能力と技術力の深さを確認",
        "tips": "使用した技術スタック、問題の切り分け方、参考にしたリソースなどを具体的に。コードの細部より思考プロセスが重要。",
        "expected_duration_seconds": 90,
    },
    {
        "target_position": "エンジニア",
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "最近使った技術や学んでいるプログラミング言語はありますか？なぜそれに興味を持ちましたか？",
        "purpose": "技術への好奇心と学習姿勢を確認",
        "tips": "学んだ理由、具体的に作ったもの、難しかった点などを含めると良い。流行だけでなく自分の関心を語る。",
        "expected_duration_seconds": 60,
    },
    {
        "target_position": "営業",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "相手を説得するために、あなたが工夫した経験を教えてください。",
        "purpose": "営業職に必要なコミュニケーション力と交渉力を確認",
        "tips": "相手の立場を理解し、共通の利益を見出したプロセスがあると良い。数字で結果を示すと説得力が増す。",
        "expected_duration_seconds": 90,
    },
    {
        "target_position": "マーケティング",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "ある商品やサービスを「もっと多くの人に知ってもらう」ために、あなたならどうしますか？具体的なアイデアを教えてください。",
        "purpose": "マーケティング思考と発想力を確認",
        "tips": "ターゲット設定、チャネル選定、KPIの仮説まで考えると良い。実体験（サークルの集客など）があれば更に良い。",
        "expected_duration_seconds": 90,
    },
    {
        "target_position": "人事",
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "「人が活躍できる組織」とは、どのような組織だと思いますか？あなたの経験を踏まえて教えてください。",
        "purpose": "人事職としての組織への関心と価値観を確認",
        "tips": "チームでのポジティブな経験、または改善したいと思った経験の両方の視点があると深みが出る。",
        "expected_duration_seconds": 90,
    },
    {
        "target_position": "経理・財務",
        "category": QuestionCategory.GENERAL,
        "difficulty": DifficultyLevel.HARD,
        "text_ja": "「正確さ」と「スピード」が両立できない場面で、あなたはどう判断しますか？具体的な経験を教えてください。",
        "purpose": "経理職に必要な正確性と判断力を確認",
        "tips": "単なる「両立」ではなく、状況に応じた優先順位の付け方と、その判断基準を語る。",
        "expected_duration_seconds": 90,
    },

    # ======== 文理別質問 ========
    {
        "target_industry": "理系",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "研究活動（卒論・修論）で取り組んでいるテーマと、その社会的意義について教えてください。",
        "purpose": "理系学生の研究内容と論理的思考力を確認",
        "tips": "専門用語を使いすぎず、文系の面接官にも伝わるように説明する力が問われる。研究の「なぜ」を明確に。",
        "expected_duration_seconds": 90,
    },
    {
        "target_industry": "文系",
        "category": QuestionCategory.GAKUCHIKA,
        "difficulty": DifficultyLevel.MEDIUM,
        "text_ja": "文系の学びの中で、社会に出て最も役立つと思うスキルは何ですか？",
        "purpose": "文系学生の学びと実社会の接続を確認",
        "tips": "批判的思考、データ分析、文章作成、異文化理解など、具体的なスキルを挙げ、その根拠を説明する。",
        "expected_duration_seconds": 60,
    },
]


def seed_company_questions():
    """企業別質問をDBに追加（重複を避ける）"""
    db = SessionLocal()
    try:
        existing = db.query(Question).filter(Question.target_company != "").count()
        if existing > 0:
            print(f"既に{existing}件の企業別質問があります。スキップします。")
            return

        max_order = db.query(Question.order_index).order_by(
            Question.order_index.desc()
        ).first()
        start_order = (max_order[0] + 1) if max_order else 0

        for i, q_data in enumerate(COMPANY_QUESTIONS):
            q = Question(
                order_index=start_order + i,
                **{k: v for k, v in q_data.items()},
            )
            db.add(q)

        db.commit()
        print(f"✅ {len(COMPANY_QUESTIONS)}件の企業別質問を追加しました！")
        print(f"   対象企業/業界: 楽天、メルカリ、アクセンチュア、LINE")
        print(f"   対象業界: コンサル（ケース問題）、金融、メーカー、広告")
    finally:
        db.close()


if __name__ == "__main__":
    seed_company_questions()
