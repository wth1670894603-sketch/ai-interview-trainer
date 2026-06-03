'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { User } from '@/types'
import { ChevronLeft, Users, BarChart3, BookOpen, Shield, ShieldOff, XCircle } from 'lucide-react'
import { formatDate } from '@/lib/utils'

interface AdminStats {
  total_users: number
  active_users: number
  total_interviews: number
  completed_interviews: number
  total_questions: number
}

interface AdminUser {
  id: string
  email: string
  username: string
  display_name: string
  university: string
  grade: string
  is_active: boolean
  is_admin: boolean
  interview_count: number
  created_at: string
}

export default function AdminPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [users, setUsers] = useState<AdminUser[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    loadData()
  }, [router])

  async function loadData() {
    try {
      const [profile, statsData, usersData] = await Promise.all([
        api.getProfile(),
        api.request<AdminStats>('/api/user/admin/stats'),
        api.request<AdminUser[]>('/api/user/admin/users'),
      ])
      setUser(profile)
      setStats(statsData)
      setUsers(usersData)
    } catch (err: any) {
      if (err.message?.includes('403')) {
        setError('管理者権限がありません')
      } else {
        setError(err.message || '読み込みに失敗しました')
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleToggleAdmin(userId: string) {
    try {
      await api.request(`/api/user/admin/users/${userId}/toggle-admin`, { method: 'PATCH' })
      loadData()
    } catch (err: any) {
      alert(err.message)
    }
  }

  async function handleToggleActive(userId: string) {
    try {
      await api.request(`/api/user/admin/users/${userId}/deactivate`, { method: 'PATCH' })
      loadData()
    } catch (err: any) {
      alert(err.message)
    }
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <XCircle size={48} className="mx-auto mb-4 text-red-400" />
          <p className="text-red-500 mb-4">{error}</p>
          <button onClick={() => router.push('/dashboard')} className="text-blue-600 hover:underline cursor-pointer">
            ダッシュボードに戻る
          </button>
        </div>
      </div>
    )
  }

  if (loading || !stats) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center gap-3">
          <button onClick={() => router.push('/dashboard')} className="p-1 hover:bg-slate-100 rounded-lg cursor-pointer">
            <ChevronLeft size={20} />
          </button>
          <h1 className="text-lg font-semibold">管理画面</h1>
          <span className="text-xs px-2 py-0.5 bg-red-50 text-red-600 rounded-full">管理者</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* 統計 */}
        <div className="grid grid-cols-5 gap-4 mb-8">
          {[
            { icon: Users, label: '総ユーザー', value: stats.total_users, color: 'text-blue-600', bg: 'bg-blue-50' },
            { icon: Users, label: 'アクティブ', value: stats.active_users, color: 'text-green-600', bg: 'bg-green-50' },
            { icon: BarChart3, label: '面接(総)', value: stats.total_interviews, color: 'text-purple-600', bg: 'bg-purple-50' },
            { icon: BarChart3, label: '面接(完了)', value: stats.completed_interviews, color: 'text-amber-600', bg: 'bg-amber-50' },
            { icon: BookOpen, label: '質問数', value: stats.total_questions, color: 'text-rose-600', bg: 'bg-rose-50' },
          ].map((item, i) => (
            <div key={i} className="bg-white rounded-xl border p-4">
              <div className={`w-8 h-8 ${item.bg} rounded-lg flex items-center justify-center mb-2`}>
                <item.icon size={16} className={item.color} />
              </div>
              <p className="text-xs text-slate-500">{item.label}</p>
              <p className="text-xl font-bold">{item.value}</p>
            </div>
          ))}
        </div>

        {/* ユーザー一覧 */}
        <h2 className="text-lg font-semibold mb-4">ユーザー一覧（{users.length}件）</h2>
        <div className="bg-white rounded-xl border overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 border-b">
              <tr>
                <th className="text-left px-4 py-3 font-medium text-slate-500">ユーザー</th>
                <th className="text-left px-4 py-3 font-medium text-slate-500">メール</th>
                <th className="text-left px-4 py-3 font-medium text-slate-500">大学</th>
                <th className="text-center px-4 py-3 font-medium text-slate-500">面接数</th>
                <th className="text-center px-4 py-3 font-medium text-slate-500">権限</th>
                <th className="text-center px-4 py-3 font-medium text-slate-500">状態</th>
                <th className="text-left px-4 py-3 font-medium text-slate-500">登録日</th>
                <th className="text-center px-4 py-3 font-medium text-slate-500">操作</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} className="border-b last:border-0 hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-medium">{u.display_name || u.username}</div>
                    <div className="text-xs text-slate-400">@{u.username}</div>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{u.email}</td>
                  <td className="px-4 py-3 text-slate-500">{u.university || '-'}</td>
                  <td className="px-4 py-3 text-center font-medium">{u.interview_count}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${u.is_admin ? 'bg-red-50 text-red-600' : 'bg-slate-100 text-slate-500'}`}>
                      {u.is_admin ? '管理者' : 'ユーザー'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${u.is_active ? 'bg-green-50 text-green-600' : 'bg-slate-100 text-slate-400'}`}>
                      {u.is_active ? '有効' : '無効'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-500 text-xs">{formatDate(u.created_at)}</td>
                  <td className="px-4 py-3">
                    <div className="flex justify-center gap-2">
                      <button
                        onClick={() => handleToggleAdmin(u.id)}
                        className="p-1.5 hover:bg-slate-100 rounded cursor-pointer"
                        title={u.is_admin ? '管理者権限を剥奪' : '管理者にする'}
                      >
                        {u.is_admin ? <ShieldOff size={14} className="text-red-500" /> : <Shield size={14} className="text-slate-400" />}
                      </button>
                      <button
                        onClick={() => handleToggleActive(u.id)}
                        className="p-1.5 hover:bg-slate-100 rounded cursor-pointer"
                        title={u.is_active ? '無効化' : '再有効化'}
                      >
                        <XCircle size={14} className={u.is_active ? 'text-slate-400' : 'text-green-500'} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
