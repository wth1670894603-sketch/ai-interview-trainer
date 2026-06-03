'use client'

import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const [isRegister, setIsRegister] = useState(false)
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (isRegister) {
        await api.register({ email, username, password })
      }
      await api.login(email, password)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message || 'エラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900">AI面接トレーナー</h1>
          <p className="text-slate-500 mt-2">日本大学生のためのAI面接練習</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-sm border p-8 space-y-5">
          <h2 className="text-xl font-semibold text-center">
            {isRegister ? '新規登録' : 'ログイン'}
          </h2>

          {error && (
            <div className="bg-red-50 text-red-600 text-sm rounded-lg p-3 text-center">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">メールアドレス</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none transition"
              placeholder="student@university.ac.jp"
              required
            />
          </div>

          {isRegister && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">ユーザー名</label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none transition"
                placeholder="taro_yamada"
                required
                minLength={2}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">パスワード</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none transition"
              placeholder="••••••••"
              required
              minLength={6}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition cursor-pointer"
          >
            {loading ? '処理中...' : isRegister ? 'アカウント作成' : 'ログイン'}
          </button>

          <div className="text-center text-sm text-slate-500">
            {isRegister ? (
              <>既にアカウントをお持ちですか？{' '}
                <button type="button" onClick={() => setIsRegister(false)} className="text-blue-600 hover:underline cursor-pointer">
                  ログイン
                </button>
              </>
            ) : (
              <>アカウントがありませんか？{' '}
                <button type="button" onClick={() => setIsRegister(true)} className="text-blue-600 hover:underline cursor-pointer">
                  新規登録
                </button>
              </>
            )}
          </div>
        </form>
      </div>
    </div>
  )
}
