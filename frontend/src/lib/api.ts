/* API クライアント */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private token: string | null = null

  constructor() {
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('token')
    }
  }

  setToken(token: string) {
    this.token = token
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token)
    }
  }

  clearToken() {
    this.token = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token')
    }
  }

  async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
    })

    if (res.status === 401) {
      this.clearToken()
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
      throw new Error('認証が必要です')
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'エラーが発生しました' }))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }

    return res.json()
  }

  /* 認証 */
  async register(data: { email: string; username: string; password: string }) {
    return this.request<import('@/types').AuthResponse>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async login(email: string, password: string) {
    const res = await this.request<import('@/types').AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    this.setToken(res.access_token)
    return res
  }

  /* ユーザー */
  async getProfile() {
    return this.request<import('@/types').User>('/api/user/me')
  }

  /* 面接 */
  async createInterview(data: Partial<import('@/types').InterviewFormData>) {
    return this.request<import('@/types').Interview>('/api/interviews', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getInterviews() {
    return this.request<import('@/types').Interview[]>('/api/interviews')
  }

  async getInterview(id: string) {
    return this.request<import('@/types').Interview>(`/api/interviews/${id}`)
  }

  async startInterview(id: string) {
    return this.request<import('@/types').InterviewStartResponse>(
      `/api/interviews/${id}/start`,
      { method: 'POST' }
    )
  }

  async submitAnswer(
    interviewId: string,
    order: number,
    answer_text: string,
    answer_duration_seconds: number = 0
  ) {
    return this.request<import('@/types').InterviewQuestion>(
      `/api/interviews/${interviewId}/questions/${order}/answer`,
      {
        method: 'POST',
        body: JSON.stringify({ answer_text, answer_duration_seconds }),
      }
    )
  }

  async getNextQuestion(interviewId: string, currentOrder: number) {
    return this.request<import('@/types').InterviewQuestion>(
      `/api/interviews/${interviewId}/next/${currentOrder}`
    )
  }

  async completeInterview(interviewId: string) {
    return this.request<import('@/types').Interview>(
      `/api/interviews/${interviewId}/complete`,
      { method: 'POST' }
    )
  }

  /* 評価 */
  async evaluateInterview(interviewId: string) {
    return this.request<import('@/types').BatchEvaluation>(
      `/api/evaluations/interviews/${interviewId}/complete`,
      { method: 'POST' }
    )
  }

  /* 音声回答 */
  async submitAudioAnswer(interviewId: string, order: number, blob: Blob) {
    const formData = new FormData()
    formData.append('file', blob, 'answer.webm')

    const headers: Record<string, string> = {}
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const res = await fetch(`${API_BASE}/api/interviews/${interviewId}/questions/${order}/answer/audio`, {
      method: 'POST',
      headers,
      body: formData,
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: '音声認識に失敗しました' }))
      throw new Error(err.detail || `HTTP ${res.status}`)
    }

    return res.json()
  }
}

export const api = new ApiClient()
