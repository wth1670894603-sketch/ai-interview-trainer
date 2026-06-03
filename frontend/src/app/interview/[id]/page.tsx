'use client'

import { useEffect, useState, useRef, useCallback } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { api } from '@/lib/api'
import { Interview, InterviewQuestion, BatchEvaluation } from '@/types'
import { categoryLabel, scoreColor } from '@/lib/utils'
import {
  Mic, MicOff, Send, ArrowRight, CheckCircle, Loader2,
  Clock, Star, MessageSquare, ChevronLeft, Square, Play,
  Gauge, Volume2, MessageCircle,
} from 'lucide-react'

type Phase = 'loading' | 'ready' | 'question' | 'answering' | 'evaluating' | 'feedback' | 'completed'

export default function InterviewSessionPage() {
  const router = useRouter()
  const params = useParams()
  const interviewId = params.id as string

  const [interview, setInterview] = useState<Interview | null>(null)
  const [currentQ, setCurrentQ] = useState<InterviewQuestion | null>(null)
  const [phase, setPhase] = useState<Phase>('loading')
  const [answerText, setAnswerText] = useState('')
  const [evaluation, setEvaluation] = useState<BatchEvaluation | null>(null)
  const [voiceMetrics, setVoiceMetrics] = useState<any>(null)
  const [error, setError] = useState('')
  const [questionIndex, setQuestionIndex] = useState(0)
  const [totalQuestions, setTotalQuestions] = useState(0)
  const [startTime, setStartTime] = useState<number>(0)
  const [elapsed, setElapsed] = useState(0)
  const textAreaRef = useRef<HTMLTextAreaElement>(null)

  // 面接データの初期化
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    api.getInterview(interviewId).then(iv => {
      setInterview(iv)
      const answeredCount = iv.questions.filter(q => q.answer_text).length
      setQuestionIndex(answeredCount)
      setTotalQuestions(iv.question_count)

      if (iv.status === 'in_progress') {
        const unanswered = iv.questions.find(q => !q.answer_text)
        if (unanswered) {
          setCurrentQ(unanswered)
          setPhase('question')
          return
        }
      }
      if (iv.status === 'completed') {
        setPhase('completed')
        api.evaluateInterview(interviewId).then(ev => {
          setEvaluation(ev)
        }).catch(() => {})
        return
      }
      // pending: 開始
      setPhase('ready')
    }).catch(err => {
      setError(err.message)
      setPhase('ready')
    })
  }, [interviewId, router])

  // 経過時間
  useEffect(() => {
    if (phase !== 'answering') return
    const interval = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTime) / 1000))
    }, 200)
    return () => clearInterval(interval)
  }, [phase, startTime])

  // 面接開始
  async function handleStart() {
    setPhase('loading')
    try {
      const res = await api.startInterview(interviewId)
      setCurrentQ(res.question)
      setTotalQuestions(res.total_questions)
      setQuestionIndex(0)
      setPhase('question')
    } catch (err: any) {
      setError(err.message)
    }
  }

  // 回答を始める
  function handleStartAnswer() {
    setPhase('answering')
    setStartTime(Date.now())
    setElapsed(0)
    setTimeout(() => textAreaRef.current?.focus(), 100)
  }

  // 回答提出
  async function handleSubmit() {
    if (!answerText.trim() || !currentQ) return

    const duration = Math.floor((Date.now() - startTime) / 1000)
    setPhase('evaluating')

    try {
      await api.submitAnswer(interviewId, currentQ.order_index, answerText, duration)

      // 次の質問があるか
      try {
        const nextQ = await api.getNextQuestion(interviewId, currentQ.order_index)
        setCurrentQ(nextQ)
        setQuestionIndex(nextQ.order_index)
        setAnswerText('')
        setPhase('question')
      } catch {
        // 最後の質問 → 完了
        await api.completeInterview(interviewId)
        setPhase('evaluating')
        const ev = await api.evaluateInterview(interviewId)
        setEvaluation(ev)
        setPhase('completed')
      }
    } catch (err: any) {
      setError(err.message)
    }
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <button onClick={() => router.push('/dashboard')} className="text-blue-600 hover:underline cursor-pointer">
            ダッシュボードに戻る
          </button>
        </div>
      </div>
    )
  }

  if (!interview) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 size={32} className="animate-spin text-blue-500" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* ヘッダー */}
      <header className="bg-white border-b">
        <div className="max-w-3xl mx-auto px-4 h-14 flex items-center gap-3">
          <button onClick={() => router.push('/dashboard')} className="p-1 hover:bg-slate-100 rounded-lg cursor-pointer">
            <ChevronLeft size={20} />
          </button>
          <div className="flex-1">
            <div className="text-sm font-medium">
              {interview.target_company || interview.target_industry || '面接練習'}
            </div>
            <div className="text-xs text-slate-400 flex items-center gap-2 flex-wrap">
              {phase === 'completed' ? '完了' : `${questionIndex + 1} / ${totalQuestions}問目`}
              {interview.target_position && <span>⚡{interview.target_position}</span>}
              {interview.university && <span>🏫{interview.university}</span>}
            </div>
          </div>
          {phase === 'completed' && evaluation && (
            <div className={`text-lg font-bold ${scoreColor(evaluation.overall_score)}`}>
              {Math.round(evaluation.overall_score)}
            </div>
          )}
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        {/* 準備画面 */}
        {phase === 'ready' && (
          <div className="text-center py-16">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Mic size={28} className="text-blue-600" />
            </div>
            <h2 className="text-xl font-semibold mb-2">面接を開始しますか？</h2>
            <p className="text-slate-500 mb-1">
              タイプ: {categoryLabel(interview.interview_type)} · {totalQuestions}問
            </p>
            <div className="flex justify-center gap-3 text-sm text-slate-400 mb-6">
              {interview.target_company && <span>🏢 {interview.target_company}</span>}
              {interview.target_position && <span>💼 {interview.target_position}</span>}
              {interview.major && <span>📚 {interview.major}</span>}
              {interview.university && <span>🏫 {interview.university}</span>}
              {!interview.target_company && !interview.target_position && '一般的な面接'}
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-amber-700 mb-6 text-left max-w-md mx-auto">
              <p className="font-medium mb-1">💡 面接のコツ</p>
              <ul className="space-y-1">
                <li>• 結論から話す（PREP法）</li>
                <li>• 具体的な数字やエピソードを入れる</li>
                <li>• 敬語を意識する</li>
                <li>• 1つの回答は1〜2分程度に</li>
              </ul>
            </div>
            <button
              onClick={handleStart}
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition cursor-pointer"
            >
              面接を始める
            </button>
          </div>
        )}

        {/* 質問画面 */}
        {phase === 'question' && currentQ && (
          <div className="animate-fade-in">
            <div className="bg-white rounded-2xl border p-6 mb-4">
              <div className="flex items-center gap-2 mb-3">
                <MessageSquare size={16} className="text-blue-500" />
                <span className="text-sm text-blue-600 font-medium">
                  {categoryLabel(currentQ.question_category)}
                </span>
              </div>
              <p className="text-lg font-medium leading-relaxed">
                {currentQ.question_text}
              </p>
            </div>

            <button
              onClick={handleStartAnswer}
              className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl flex items-center justify-center gap-2 transition cursor-pointer"
            >
              <Mic size={20} />
              回答を始める
            </button>
          </div>
        )}

        {/* 回答画面 */}
        {phase === 'answering' && (
          <RecordingArea
            currentQ={currentQ}
            onSubmit={handleSubmit}
            onBack={() => setPhase('question')}
            answerText={answerText}
            setAnswerText={setAnswerText}
            elapsed={elapsed}
            interviewId={interviewId}
            onAnalysis={setVoiceMetrics}
          />
        )}

        {/* 評価中 */}
        {phase === 'evaluating' && (
          <div className="text-center py-16 animate-fade-in">
            <Loader2 size={40} className="animate-spin text-blue-500 mx-auto mb-4" />
            <p className="text-slate-500">評価中...</p>
            {questionIndex < totalQuestions && (
              <p className="text-sm text-slate-400 mt-1">
                次の質問を準備しています
              </p>
            )}
          </div>
        )}

        {/* 完了画面 */}
        {phase === 'completed' && evaluation && (
          <div className="animate-fade-in">
            {/* 完了バッジ */}
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <CheckCircle size={32} className="text-green-600" />
              </div>
              <h2 className="text-xl font-semibold">面接完了</h2>
              <p className="text-slate-500">お疲れ様でした！</p>
            </div>

            {/* 総合スコア */}
            <div className="bg-white rounded-2xl border p-6 mb-6">
              <div className="text-center mb-6">
                <div className="text-sm text-slate-500 mb-1">総合スコア</div>
                <div className={`text-5xl font-bold ${scoreColor(evaluation.overall_score)}`}>
                  {Math.round(evaluation.overall_score)}
                </div>
              </div>

              {/* 各軸スコア */}
              <div className="grid grid-cols-5 gap-3 mb-6">
                {([
                  { label: '内容', key: 'content_score', score: evaluation.content_score, color: 'bg-blue-500' },
                  { label: '構成', key: 'structure_score', score: evaluation.structure_score, color: 'bg-green-500' },
                  { label: '言語', key: 'language_score', score: evaluation.language_score, color: 'bg-purple-500' },
                  { label: '熱意', key: 'passion_score', score: evaluation.passion_score, color: 'bg-amber-500' },
                  { label: 'マナー', key: 'manners_score', score: evaluation.manners_score, color: 'bg-rose-500' },
                ] as const).map(axis => (
                  <div key={axis.key} className="text-center">
                    <div className="text-xs text-slate-400 mb-1">{axis.label}</div>
                    <div className={`w-full h-1.5 bg-slate-100 rounded-full mb-1`}>
                      <div
                        className={`h-full rounded-full ${axis.color} transition-all`}
                        style={{ width: `${axis.score}%` }}
                      />
                    </div>
                    <div className={`text-sm font-semibold ${scoreColor(axis.score)}`}>
                      {Math.round(axis.score)}
                    </div>
                  </div>
                ))}
              </div>

              {/* 総評 */}
              {evaluation.feedback_summary && (
                <div className="bg-blue-50 rounded-lg p-4 text-sm text-blue-800 mb-4">
                  {evaluation.feedback_summary}
                </div>
              )}

              {/* 音声分析メトリクス */}
              {voiceMetrics && (
                <div className="border-t pt-4">
                  <h4 className="text-sm font-medium text-slate-600 mb-3 flex items-center gap-2">
                    <Volume2 size={16} /> 音声分析
                  </h4>
                  <div className="grid grid-cols-3 gap-3">
                    {/* 語速 */}
                    <div className="bg-slate-50 rounded-lg p-3">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Gauge size={14} className="text-blue-500" />
                        <span className="text-xs font-medium text-slate-500">語速</span>
                      </div>
                      <p className="text-lg font-bold">{voiceMetrics.speed?.chars_per_min || '-'}</p>
                      <p className="text-xs text-slate-400">文字/分</p>
                      <p className={`text-xs mt-1 ${voiceMetrics.speed?.optimal ? 'text-green-600' : 'text-amber-600'}`}>
                        {voiceMetrics.speed?.judgment || ''}
                      </p>
                    </div>

                    {/* フィラー */}
                    <div className="bg-slate-50 rounded-lg p-3">
                      <div className="flex items-center gap-1.5 mb-1">
                        <MessageCircle size={14} className="text-purple-500" />
                        <span className="text-xs font-medium text-slate-500">フィラー</span>
                      </div>
                      <p className="text-lg font-bold">{voiceMetrics.fillers?.total || 0}</p>
                      <p className="text-xs text-slate-400">回（えー・あのー等）</p>
                      {voiceMetrics.fillers?.fillers && Object.entries(voiceMetrics.fillers.fillers).map(([w, c]) => (
                        <span key={w} className="text-xs text-slate-500 mr-1">「{w}」×{String(c)}</span>
                      ))}
                    </div>

                    {/* 敬語 */}
                    <div className="bg-slate-50 rounded-lg p-3">
                      <div className="flex items-center gap-1.5 mb-1">
                        <MessageSquare size={14} className="text-emerald-500" />
                        <span className="text-xs font-medium text-slate-500">敬語</span>
                      </div>
                      <p className={`text-lg font-bold ${(voiceMetrics.keigo?.score || 0) >= 70 ? 'text-green-600' : 'text-amber-600'}`}>
                        {voiceMetrics.keigo?.score || 0}
                      </p>
                      <p className="text-xs text-slate-400">/ 100点</p>
                      {voiceMetrics.keigo?.issues?.map((i: string, k: number) => (
                        <p key={k} className="text-xs text-red-500 mt-0.5">⚠ {i}</p>
                      ))}
                    </div>
                  </div>
                  {voiceMetrics.keigo?.suggestions?.length > 0 && (
                    <div className="mt-2 bg-green-50 rounded-lg p-2 text-xs text-green-700">
                      💡 {voiceMetrics.keigo.suggestions.join(' / ')}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* 各質問の詳細 */}
            <h3 className="font-semibold mb-4">質問別フィードバック</h3>
            <div className="space-y-4 mb-8">
              {evaluation.question_evaluations.map((ev, idx) => (
                <div key={ev.id} className="bg-white rounded-xl border p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <span className="text-xs text-blue-600 font-medium">
                        Q{idx + 1}
                      </span>
                      <p className="text-sm mt-1">{ev.interview_question_id}</p>
                    </div>
                    <div className={`text-lg font-bold ${scoreColor(ev.overall_score)}`}>
                      {Math.round(ev.overall_score)}
                    </div>
                  </div>

                  <div className="text-sm space-y-2">
                    {ev.content_feedback && (
                      <p><span className="text-slate-500">内容:</span> {ev.content_feedback}</p>
                    )}
                    {ev.structure_feedback && (
                      <p><span className="text-slate-500">構成:</span> {ev.structure_feedback}</p>
                    )}
                    {ev.language_feedback && (
                      <p><span className="text-slate-500">言語:</span> {ev.language_feedback}</p>
                    )}
                  </div>

                  {ev.strengths.length > 0 && (
                    <div className="mt-3">
                      <p className="text-sm font-medium text-green-600 mb-1">👍 良かった点</p>
                      <ul className="list-disc list-inside text-sm text-slate-600 space-y-0.5">
                        {ev.strengths.map((s, i) => <li key={i}>{s}</li>)}
                      </ul>
                    </div>
                  )}

                  {ev.suggested_answer_points.length > 0 && (
                    <div className="mt-3 p-3 bg-amber-50 rounded-lg">
                      <p className="text-sm font-medium text-amber-700 mb-1">💡 参考回答のポイント</p>
                      <ul className="list-disc list-inside text-sm text-amber-800 space-y-0.5">
                        {ev.suggested_answer_points.map((p, i) => <li key={i}>{p}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* アクションボタン */}
            <div className="flex gap-3">
              <button
                onClick={() => router.push('/dashboard')}
                className="flex-1 py-3 border border-slate-200 rounded-xl hover:bg-slate-50 transition cursor-pointer"
              >
                ダッシュボード
              </button>
              <button
                onClick={() => router.push('/dashboard')}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition cursor-pointer"
              >
                もう一度練習
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

/* 音声録音 + テキスト入力 コンポーネント */
function RecordingArea({currentQ, onSubmit, onBack, answerText, setAnswerText, elapsed, interviewId, onAnalysis}: {
  currentQ: InterviewQuestion | null
  onSubmit: () => void
  onBack: () => void
  answerText: string
  setAnswerText: (v: string) => void
  elapsed: number
  interviewId: string
  onAnalysis?: (v: any) => void
}) {
  const [recording, setRecording] = useState(false)
  const [transcribing, setTranscribing] = useState(false)
  const mediaRecorder = useRef<MediaRecorder | null>(null)
  const chunks = useRef<Blob[]>([])

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' })
      mediaRecorder.current = recorder
      chunks.current = []

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.current.push(e.data)
      }

      recorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop())
        const blob = new Blob(chunks.current, { type: 'audio/webm' })
        if (blob.size < 1000) return

        setTranscribing(true)
        try {
          const result = await api.submitAudioAnswer(interviewId, currentQ?.order_index ?? 0, blob)
          setAnswerText(result.transcript || '')
          if (result.analysis) onAnalysis?.(result.analysis)
        } catch (err: any) {
          console.error('STT failed:', err)
        } finally {
          setTranscribing(false)
        }
      }

      recorder.start()
      setRecording(true)
    } catch (err) {
      alert('マイクへのアクセスを許可してください')
    }
  }

  function stopRecording() {
    mediaRecorder.current?.stop()
    setRecording(false)
  }

  return (
    <div className="animate-fade-in">
      {/* 質問（常に固定表示） */}
      <div className="bg-white rounded-2xl border p-4 mb-4">
        <div className="text-sm text-blue-600 mb-1">{categoryLabel(currentQ?.question_category || '')}</div>
        <p className="font-medium">{currentQ?.question_text}</p>
      </div>

      {/* 録音フェーズ */}
      {!recording && !transcribing && (
        <div className="flex flex-col items-center mb-4">
          <button
            onClick={startRecording}
            disabled={transcribing}
            className="w-20 h-20 rounded-full bg-red-500 hover:bg-red-600 disabled:bg-slate-300 text-white flex items-center justify-center shadow-lg transition cursor-pointer"
          >
            <Mic size={32} />
          </button>
          <p className="text-sm text-slate-500 mt-3">🎤 マイクをクリックして回答を録音</p>
          <p className="text-xs text-slate-400 mt-1">または下のテキスト欄に直接入力してもOK</p>
        </div>
      )}

      {/* 録音中 */}
      {recording && (
        <div className="flex flex-col items-center mb-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-3 h-3 rounded-full bg-red-500 recording-pulse" />
            <span className="text-sm font-medium text-red-500">録音中...</span>
            <span className="text-sm text-slate-400">{formatTime(elapsed)}</span>
          </div>
          <button
            onClick={stopRecording}
            className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl shadow-lg transition cursor-pointer"
          >
            <Square size={18} className="inline mr-2" />
            回答終了（録音を停止）
          </button>
          <p className="text-xs text-slate-400 mt-2">話し終わったらこのボタンを押してください</p>
        </div>
      )}

      {/* 文字起こし中 */}
      {transcribing && (
        <div className="flex flex-col items-center mb-6">
          <Loader2 size={32} className="animate-spin text-blue-500 mb-3" />
          <p className="text-sm text-slate-500">音声を文字に変換中...</p>
        </div>
      )}

      {/* 文字起こし結果 + 手動編集 */}
      <div className="mb-4">
        <textarea
          value={answerText}
          onChange={e => setAnswerText(e.target.value)}
          placeholder={'録音するか、ここに直接入力してください...'}
          className="w-full h-36 p-4 border border-slate-200 rounded-xl resize-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 outline-none text-sm"
        />
      </div>

      {/* 操作ボタン */}
      <div className="flex gap-3">
        <button onClick={onBack} className="px-5 py-3 border border-slate-200 rounded-xl hover:bg-slate-50 transition cursor-pointer">
          戻る
        </button>
        <button
          onClick={onSubmit}
          disabled={!answerText.trim() || transcribing}
          className="flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-xl flex items-center justify-center gap-2 transition text-base cursor-pointer"
        >
          <Send size={18} />
          回答を送信
        </button>
      </div>
    </div>
  )
}

function formatTime(s: number) {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}
