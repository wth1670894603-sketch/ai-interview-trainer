# AI面接トレーナー 🎯

日本大学生・留学生向けのAI面接練習プラットフォーム。
AIが面接官役を務め、回答をリアルタイムで評価・フィードバックします。

## 機能

- **面接シミュレーション** — 自己PR・ガクチカ・志望動機など本番同様の流れ
- **AI評価** — 内容・構成・言語・熱意・マナーの5軸でスコアリング
- **詳細フィードバック** — 改善点・強み・模範回答ポイントを提示
- **練習履歴** — スコア推移を追跡

## クイックスタート

### 1. 環境準備

```bash
# バックエンド
cd backend
pip install -r requirements.txt
python -c "from app.seed import seed_database; seed_database()"

# .env を設定（OpenAIまたはAnthropicのAPIキー）
cp .env.example .env
```

### 2. APIキー（必須）

評価にLLMを使います。どちらか一方でOK：

| プロバイダ | 設定項目 | 最小モデル |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | gpt-4o-mini |
| Anthropic | `ANTHROPIC_API_KEY` | claude-sonnet-4-20250514 |

APIキーがない場合はモック評価モードで動作します（開発用）。

### 3. 起動

**開発環境（推奨）:**
```bash
dev.bat
```

**または個別に:**
```bash
# ターミナル1: バックエンド
cd backend && uvicorn app.main:app --reload --port 8000

# ターミナル2: フロントエンド
cd frontend && npm install && npm run dev
```

### 4. アクセス

- フロントエンド: http://localhost:3000
- API ドキュメント: http://localhost:8000/docs

## プロジェクト構造

```
ai-interview-trainer/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI エントリ
│   │   ├── models/          # DBモデル
│   │   ├── routers/         # APIルート
│   │   ├── services/        # ビジネスロジック
│   │   └── schemas/         # Pydanticスキーマ
│   └── seed.py              # 初期質問データ
├── frontend/
│   └── src/
│       ├── app/             # Next.js ページ
│       ├── components/      # React コンポーネント
│       └── lib/             # API クライアント
└── docs/
    └── architecture.md
```

## 評価軸

| 軸 | 重み | 説明 |
|---|---|---|
| 内容 (Content) | 30% | 具体性・論理性・説得力 |
| 構成 (Structure) | 20% | PREP法・結論ファースト |
| 言語 (Language) | 20% | 敬語・文法・語彙 |
| 熱意 (Passion) | 15% | 志望動機の一貫性 |
| マナー (Manners) | 15% | 言葉遣い・時間配分 |

## ロードマップ

- [x] 基本面接フロー (Q&A)
- [x] AI評価エンジン
- [x] フィードバックUI
- [ ] 音声認識 (Whisper)
- [ ] 録音再生
- [ ] スコア推移グラフ
- [ ] 弱点分析ダッシュボード
- [ ] メール認証
- [ ] 留学生向け英語対応
