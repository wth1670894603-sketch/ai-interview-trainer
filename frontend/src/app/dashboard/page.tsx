'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { Interview, User } from '@/types'
import { formatDate, scoreColor, categoryLabel } from '@/lib/utils'
import { COMPANIES, POSITIONS, MAJORS, UNIVERSITIES, INDUSTRIES, OTHER_OPTION } from '@/lib/constants'
import {
  FileText, Plus, BarChart3, Target, Clock, ChevronRight,
  LogOut, UserCircle, Shield, TrendingUp,
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [interviews, setInterviews] = useState<Interview[]>([])
  const [progress, setProgress] = useState<{date:string;score:number;company:string}[]>([])
  const [loading, setLoading] = useState(true)
  const [showNewModal, setShowNewModal] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    Promise.all([
      api.getProfile(),
      api.getInterviews(),
      api.request<{date:string;score:number;company:string}[]>('/api/interviews/stats/progress'),
    ]).then(([u, ivs, p]) => {
      setUser(u)
      setInterviews(ivs)
      setProgress(p)
    }).catch(() => {
      router.push('/login')
    }).finally(() => setLoading(false))
  }, [router])

  function logout() {
    api.clearToken()
    router.push('/login')
  }

  const completedCount = interviews.filter(i => i.status === 'completed').length
  const avgScore = interviews.length > 0
    ? Math.round(
        interviews
          .filter(i => i.overall_score)
          .reduce((sum, i) => sum + (i.overall_score || 0), 0) /
        Math.max(1, interviews.filter(i => i.overall_score).length)
      )
    : 0

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* ヘッダー */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <h1 className="text-xl font-bold text-slate-900">AI面接トレーナー</h1>
          <div className="flex items-center gap-4">
            {user?.is_admin && (
            <button onClick={() => router.push('/admin')} className="flex items-center gap-1 px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 text-sm rounded-lg transition cursor-pointer">
              <Shield size={14} />
              管理
            </button>
          )}
          <span className="text-sm text-slate-500">{user?.display_name || user?.username}</span>
            <button onClick={logout} className="p-2 hover:bg-slate-100 rounded-lg transition cursor-pointer">
              <LogOut size={20} className="text-slate-400" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* 統計 */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-xl border p-5">
            <div className="flex items-center gap-3 mb-2">
              <BarChart3 size={20} className="text-blue-500" />
              <span className="text-sm text-slate-500">面接数</span>
            </div>
            <p className="text-2xl font-bold">{interviews.length}</p>
          </div>
          <div className="bg-white rounded-xl border p-5">
            <div className="flex items-center gap-3 mb-2">
              <Target size={20} className="text-green-500" />
              <span className="text-sm text-slate-500">完了</span>
            </div>
            <p className="text-2xl font-bold">{completedCount}</p>
          </div>
          <div className="bg-white rounded-xl border p-5">
            <div className="flex items-center gap-3 mb-2">
              <BarChart3 size={20} className="text-purple-500" />
              <span className="text-sm text-slate-500">平均スコア</span>
            </div>
            <p className={`text-2xl font-bold ${scoreColor(avgScore)}`}>
              {avgScore || '-'}
            </p>
          </div>
        </div>

        {/* 成長曲線 */}
        {progress.length >= 2 && (
          <div className="bg-white rounded-xl border p-5 mb-8">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp size={20} className="text-green-500" />
              <h2 className="text-lg font-semibold">成長曲線</h2>
              <span className="text-sm text-slate-400 ml-auto">
                {progress.length}回の面接
              </span>
            </div>
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={progress}>
                  <XAxis
                    dataKey="date"
                    tickFormatter={v => new Date(v).toLocaleDateString('ja-JP', {month:'short', day:'numeric'})}
                    tick={{fontSize:12}}
                  />
                  <YAxis domain={[0, 100]} tick={{fontSize:12}} />
                  <Tooltip
                    labelFormatter={v => new Date(v).toLocaleDateString('ja-JP')}
                    formatter={(v:number) => [`${Math.round(v)}点`, 'スコア']}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#2563eb"
                    strokeWidth={2}
                    dot={{fill:'#2563eb', r:4}}
                    activeDot={{r:6}}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold">面接履歴</h2>
          <button
            onClick={() => setShowNewModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition cursor-pointer"
          >
            <Plus size={18} />
            新規面接
          </button>
        </div>

        {/* 面接一覧 */}
        {interviews.length === 0 ? (
          <div className="text-center py-16 text-slate-400">
            <FileText size={48} className="mx-auto mb-4 opacity-50" />
            <p>まだ面接練習をしていません</p>
            <p className="text-sm mt-1">「新規面接」から始めましょう</p>
          </div>
        ) : (
          <div className="space-y-3">
            {interviews.map(iv => (
              <button
                key={iv.id}
                onClick={() => router.push(`/interview/${iv.id}`)}
                className="w-full bg-white rounded-xl border p-4 hover:border-blue-200 hover:shadow-sm transition text-left cursor-pointer"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-slate-900">
                        {iv.target_company || iv.target_industry || '一般的な面接'}
                      </span>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        iv.status === 'completed' ? 'bg-green-50 text-green-600' :
                        iv.status === 'in_progress' ? 'bg-yellow-50 text-yellow-600' :
                        'bg-slate-50 text-slate-500'
                      }`}>
                        {iv.status === 'completed' ? '完了' :
                         iv.status === 'in_progress' ? '進行中' : '未開始'}
                      </span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400 flex-wrap">
                      <span className="flex items-center gap-1">
                        <Clock size={12} />
                        {formatDate(iv.created_at)}
                      </span>
                      <span>{iv.question_count}問</span>
                      <span>{iv.duration_minutes}分</span>
                      <span>{categoryLabel(iv.interview_type)}</span>
                      {iv.target_position && <span>⚡{iv.target_position}</span>}
                      {iv.major && <span>📚{iv.major}</span>}
                      {iv.university && <span>🏫{iv.university}</span>}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {iv.overall_score && (
                      <span className={`text-lg font-bold ${scoreColor(iv.overall_score)}`}>
                        {Math.round(iv.overall_score)}
                      </span>
                    )}
                    <ChevronRight size={18} className="text-slate-300" />
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </main>

      {/* 新規面接モーダル */}
      {showNewModal && (
        <NewInterviewModal
          onClose={() => setShowNewModal(false)}
          onCreated={(iv) => {
            setShowNewModal(false)
            router.push(`/interview/${iv.id}`)
          }}
        />
      )}
    </div>
  )
}

function NewInterviewModal({
  onClose,
  onCreated,
}: {
  onClose: () => void
  onCreated: (iv: Interview) => void
}) {
  const [company, setCompany] = useState('')
  const [companyOther, setCompanyOther] = useState('')
  const [position, setPosition] = useState('')
  const [positionOther, setPositionOther] = useState('')
  const [industry, setIndustry] = useState('')
  const [industryOther, setIndustryOther] = useState('')
  const [major, setMajor] = useState('')
  const [majorOther, setMajorOther] = useState('')
  const [university, setUniversity] = useState('')
  const [universityOther, setUniversityOther] = useState('')
  const [type, setType] = useState('individual')
  const [questionCount, setQuestionCount] = useState(5)
  const [duration, setDuration] = useState(15)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function resolveValue(val: string, otherVal: string): string {
    return val === '__other__' ? otherVal : val
  }

  async function handleCreate() {
    setLoading(true)
    setError('')
    try {
      const iv = await api.createInterview({
        target_company: resolveValue(company, companyOther),
        target_position: resolveValue(position, positionOther),
        target_industry: resolveValue(industry, industryOther),
        major: resolveValue(major, majorOther),
        university: resolveValue(university, universityOther),
        interview_type: type,
        question_count: questionCount,
        duration_minutes: duration,
      })
      onCreated(iv)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function renderSelectWithOther(
    val: string, setVal: (v: string) => void,
    otherVal: string, setOtherVal: (v: string) => void,
    label: string, options: {value:string;label:string}[]
  ) {
    const showOther = val === '__other__'
    return (
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">{label}</label>
        <select
          value={val}
          onChange={e => setVal(e.target.value)}
          className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none bg-white"
        >
          {options.map(o => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
        {showOther && (
          <input
            type="text"
            value={otherVal}
            onChange={e => setOtherVal(e.target.value)}
            className="mt-2 w-full px-3 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none"
            placeholder={`${label}を入力`}
            autoFocus
          />
        )}
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-lg animate-slide-up" style={{maxHeight:'85vh', overflow:'auto'}}>
        <h3 className="text-lg font-semibold mb-5">新しい面接を作成</h3>

        {error && (
          <div className="bg-red-50 text-red-600 text-sm rounded-lg p-3 mb-4">{error}</div>
        )}

        <div className="space-y-4">
          {/* ヘルパー: Select + Other */}
          {renderSelectWithOther(company, setCompany, companyOther, setCompanyOther, '志望企業', COMPANIES)}
          {renderSelectWithOther(position, setPosition, positionOther, setPositionOther, '志望職種', POSITIONS)}
          {renderSelectWithOther(industry, setIndustry, industryOther, setIndustryOther, '志望業界', INDUSTRIES)}

          {/* 面接タイプ */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">面接タイプ</label>
            <select
              value={type}
              onChange={e => setType(e.target.value)}
              className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none bg-white"
            >
              <option value="individual">個人面接</option>
              <option value="group">集団面接</option>
              <option value="case">ケース面接</option>
              <option value="reverse">逆質問練習</option>
            </select>
          </div>

          {renderSelectWithOther(university, setUniversity, universityOther, setUniversityOther, '大学', UNIVERSITIES)}
          {renderSelectWithOther(major, setMajor, majorOther, setMajorOther, '学部・学科', MAJORS)}

          {/* 質問数 • 時間 */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">質問数</label>
              <select
                value={questionCount}
                onChange={e => setQuestionCount(Number(e.target.value))}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none bg-white"
              >
                {[3, 5, 7, 10].map(n => (
                  <option key={n} value={n}>{n}問</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">時間</label>
              <select
                value={duration}
                onChange={e => setDuration(Number(e.target.value))}
                className="w-full px-3 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none bg-white"
              >
                {[10, 15, 20, 30].map(n => (
                  <option key={n} value={n}>{n}分</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={onClose}
            className="flex-1 py-2 border border-slate-200 rounded-lg hover:bg-slate-50 transition cursor-pointer"
          >
            キャンセル
          </button>
          <button
            onClick={handleCreate}
            disabled={loading}
            className="flex-1 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg transition cursor-pointer"
          >
            {loading ? '作成中...' : '面接を開始'}
          </button>
        </div>
      </div>
    </div>
  )
}
