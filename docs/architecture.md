# AI面接トレーナー — アーキテクチャ

## 概要

日本大学生（留学生含む）向けのAI面接練習Webアプリ。
AIが面接官役を務め、ユーザーの回答をリアルタイム評価。

## 技術スタック

| 層 | 技術 |
|---|---|
| フロントエンド | Next.js 14 (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| バックエンド | FastAPI (Python 3.12+) |
| DB | PostgreSQL (本番) / SQLite (開発) |
| STT | Whisper (faster-whisper 最適化) |
| LLM | GPT-4o / Claude API (評価エンジン) |
| TTS | VoiceVox (日本語) / ElevenLabs (オプション) |
| 認証 | JWT + OAuth2 (Google/GitHub) |
| インフラ | Docker Compose → ECS/Fly.io |

## データフロー

```
[ユーザー] → [WebRTC録音] → [Whisper STT] → [LLM評価]
                                                 ↓
[ユーザー] ← [フィードバック表示] ← [評価結果DB保存]
```

## 面接評価軸

| 軸 | 重み | 評価内容 |
|---|---|---|
| 内容 (Content) | 30% | 回答の論理性、具体性、説得力 |
| 構成 (Structure) | 20% | PREP法、結論ファースト |
| 日本語 (Language) | 20% | 敬語、文法、語彙の適切さ |
| 熱意 (Passion) | 15% | 志望動機の一貫性、説得力 |
| マナー (Manners) | 15% | 面接マナー、時間配分、言葉遣い |

## 質問カテゴリ

1. **自己PR** — 強み・弱み、学生時代の挑戦
2. **ガクチカ** — 学生時代に力を入れたこと
3. **志望動機** — 業界研究、企業理解
4. **逆質問** — 志望度の高さを示す質問
5. **ケース・フェルミ** — 論理的思考（外資系向け）
6. **GD風** — グループディスカッション練習

## ディレクトリ構成

```
ai-interview-trainer/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI エントリポイント
│   │   ├── config.py         # 設定管理
│   │   ├── database.py       # DB接続
│   │   ├── models/           # SQLAlchemy モデル
│   │   ├── routers/          # API ルート
│   │   ├── services/         # ビジネスロジック
│   │   └── schemas/          # Pydantic スキーマ
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # React コンポーネント
│   │   ├── lib/              # ユーティリティ
│   │   └── types/            # TypeScript 型定義
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── docs/
    └── architecture.md
```

## フェーズ計画

### Phase 1 — MVP (2週間)
- 認証 (JWT / OAuth)
- 面接セッション作成・管理
- AI面接官 Q&A (テキストベース)
- スコアリングとフィードバック
- 基本UI (ダッシュボード + 面接画面)

### Phase 2 — 音声・録画 (＋1週間)
- WebRTC録音 → Whisper STT
- 音声フィードバック (VoiceVox)
- 回答履歴再生

### Phase 3 — 分析・成長 (＋1週間)
- 弱点分析ダッシュボード
- 時系列スコア推移
- 練習計画レコメンド

### Phase 4 — 本番 (＋1週間)
- テスト・パフォーマンス最適化
- デプロイメント
- 日本語UI完全対応
