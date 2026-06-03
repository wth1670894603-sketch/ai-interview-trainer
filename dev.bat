@echo off
chcp 65001 >nul
echo ========================================
echo  AI面接トレーナー - 開発起動
echo ========================================
echo.

:: バックエンド起動
echo [1/3] バックエンドの準備...
cd backend
if not exist "data" mkdir data
if not exist ".env" copy .env.example .env >nul 2>&1

:: 依存関係インストール
pip install -r requirements.txt >nul 2>&1
echo ✓ バックエンド依存関係 OK

:: シードデータ投入
python -c "from app.seed import seed_database; seed_database()" >nul 2>&1
echo ✓ シードデータ OK

:: バックエンド起動
start "backend" cmd /c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ✓ バックエンド起動 (http://localhost:8000)
cd ..

:: フロントエンド起動
echo [2/3] フロントエンドの準備...
cd frontend
if not exist "node_modules" (
    call npm install
)
echo ✓ フロントエンド依存関係 OK

:: フロントエンド起動
start "frontend" cmd /c "npm run dev"
echo ✓ フロントエンド起動 (http://localhost:3000)
cd ..

echo.
echo ========================================
echo  起動完了！
echo  フロントエンド: http://localhost:3000
echo  バックエンドAPI: http://localhost:8000
echo  API ドキュメント: http://localhost:8000/docs
echo ========================================
