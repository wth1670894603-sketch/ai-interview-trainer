'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { ChevronLeft, Plus, Trash2, FileText, MessageSquare, Loader2 } from 'lucide-react'
import { formatDate } from '@/lib/utils'

interface ESItem {
  id: string
  title: string
  category: string
  content: string
  target_company: string
  target_position: string
  created_at: string
}

interface GeneratedQuestion {
  question_text: string
  purpose: string
  tips: string
}

const CATEGORIES = [
  { value: 'gakuchika', label: 'ガクチカ（学生時代に力を入れたこと）' },
  { value: 'self_pr', label: '自己PR' },
  { value: 'motivation', label: '志望動機' },
  { value: 'other', label: 'その他' },
]

export default function ESPage() {
  const router = useRouter()
  const [entries, setEntries] = useState<ESItem[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [questions, setQuestions] = useState<GeneratedQuestion[]>([])
  const [generating, setGenerating] = useState('')

  const [form, setForm] = useState({ title: '', category: 'gakuchika', content: '', target_company: '', target_position: '' })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/login'); return }
    loadES()
  }, [router])

  async function loadES() {
    try {
      const data = await api.request<ESItem[]>('/api/es')
      setEntries(data)
    } catch { /* ignore */ }
    setLoading(false)
  }

  async function handleSave() {
    if (!form.title.trim() || !form.content.trim()) return
    setSaving(true)
    try {
      await api.request('/api/es', {
        method: 'POST',
        body: JSON.stringify(form),
      })
      setShowForm(false)
      setForm({ title: '', category: 'gakuchika', content: '', target_company: '', target_position: '' })
      loadES()
    } catch (err: any) { alert(err.message) }
    setSaving(false)
  }

  async function handleDelete(id: string) {
    try {
      await api.request(`/api/es/${id}`, { method: 'DELETE' })
      loadES()
    } catch (err: any) { alert(err.message) }
  }

  async function handleGenerate(id: string) {
    setGenerating(id)
    try {
      const data = await api.request<{ questions: GeneratedQuestion[] }>(`/api/es/${id}/generate`, { method: 'POST' })
      setQuestions(data.questions || [])
    } catch (err: any) { alert(err.message) }
    setGenerating('')
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b">
        <div className="max-w-3xl mx-auto px-4 h-14 flex items-center gap-3">
          <button onClick={() => router.push('/dashboard')} className="p-1 hover:bg-slate-100 rounded-lg cursor-pointer">
            <ChevronLeft size={20} />
          </button>
          <h1 className="text-lg font-semibold">ES（エントリーシート）管理</h1>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-6">
        {/* 登録ボタン */}
        <div className="flex justify-end mb-6">
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition cursor-pointer"
          >
            <Plus size={18} /> ESを追加
          </button>
        </div>

        {/* 登録フォーム */}
        {showForm && (
          <div className="bg-white rounded-xl border p-5 mb-6 animate-slide-up">
            <h2 className="font-semibold mb-4">新しいESを登録</h2>
            <div className="space-y-3">
              <input
                value={form.title}
                onChange={e => setForm({ ...form, title: e.target.value })}
                placeholder="タイトル（例: 学園祭実行委員会）"
                className="w-full px-3 py-2 border rounded-lg text-sm focus:border-blue-400 outline-none"
              />
              <select
                value={form.category}
                onChange={e => setForm({ ...form, category: e.target.value })}
                className="w-full px-3 py-2 border rounded-lg text-sm bg-white outline-none"
              >
                {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
              </select>
              <textarea
                value={form.content}
                onChange={e => setForm({ ...form, content: e.target.value })}
                placeholder="ESの本文を入力（ガクチカ・自己PR・志望動機など）"
                rows={6}
                className="w-full px-3 py-2 border rounded-lg text-sm resize-none outline-none focus:border-blue-400"
              />
              <div className="grid grid-cols-2 gap-3">
                <input value={form.target_company} onChange={e => setForm({ ...form, target_company: e.target.value })} placeholder="志望企業（任意）" className="w-full px-3 py-2 border rounded-lg text-sm outline-none" />
                <input value={form.target_position} onChange={e => setForm({ ...form, target_position: e.target.value })} placeholder="志望職種（任意）" className="w-full px-3 py-2 border rounded-lg text-sm outline-none" />
              </div>
              <div className="flex gap-3 pt-2">
                <button onClick={() => setShowForm(false)} className="px-4 py-2 border rounded-lg text-sm hover:bg-slate-50 cursor-pointer">キャンセル</button>
                <button onClick={handleSave} disabled={saving} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-lg text-sm cursor-pointer">
                  {saving ? '保存中...' : '保存'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ES一覧 */}
        {loading ? (
          <div className="text-center py-12"><Loader2 size={24} className="animate-spin mx-auto text-blue-500" /></div>
        ) : entries.length === 0 ? (
          <div className="text-center py-16 text-slate-400">
            <FileText size={48} className="mx-auto mb-3 opacity-50" />
            <p>まだESを登録していません</p>
            <p className="text-xs mt-1">ガクチカ・自己PR・志望動機を登録して、AIに面接質問を生成させよう</p>
          </div>
        ) : (
          <div className="space-y-4">
            {entries.map(es => (
              <div key={es.id} className="bg-white rounded-xl border p-5">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h3 className="font-medium">{es.title}</h3>
                    <div className="flex gap-2 text-xs text-slate-400 mt-1">
                      <span className="px-1.5 py-0.5 bg-blue-50 text-blue-600 rounded">{CATEGORIES.find(c => c.value === es.category)?.label || es.category}</span>
                      <span>{formatDate(es.created_at)}</span>
                      {es.target_company && <span>🏢 {es.target_company}</span>}
                    </div>
                  </div>
                  <button onClick={() => handleDelete(es.id)} className="p-1 hover:bg-red-50 rounded cursor-pointer">
                    <Trash2 size={14} className="text-slate-300 hover:text-red-500" />
                  </button>
                </div>
                <p className="text-sm text-slate-600 line-clamp-2">{es.content}</p>
                <div className="mt-3">
                  <button
                    onClick={() => handleGenerate(es.id)}
                    disabled={generating === es.id}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 text-xs rounded-lg transition cursor-pointer disabled:opacity-50"
                  >
                    {generating === es.id ? <Loader2 size={12} className="animate-spin" /> : <MessageSquare size={12} />}
                    AIが質問を生成
                  </button>
                </div>

                {/* 生成された質問 */}
                {questions.length > 0 && generating !== es.id && (
                  <div className="mt-3 p-3 bg-indigo-50 rounded-lg">
                    <p className="text-xs font-medium text-indigo-600 mb-2">💡 AIが生成した質問</p>
                    <div className="space-y-2">
                      {questions.map((q, i) => (
                        <div key={i} className="text-sm">
                          <p className="font-medium">Q{i + 1}. {q.question_text}</p>
                          {q.purpose && <p className="text-xs text-slate-500">🎯 {q.purpose}</p>}
                          {q.tips && <p className="text-xs text-slate-400">💡 {q.tips}</p>}
                        </div>
                      ))}
                    </div>
                    <button
                      onClick={() => {
                        const text = questions.map(q => q.question_text).join('\n')
                        navigator.clipboard.writeText(text)
                      }}
                      className="mt-2 text-xs text-indigo-500 hover:underline"
                    >
                      📋 質問をコピー
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
