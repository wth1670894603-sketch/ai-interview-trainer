/* 型定義 */

export interface User {
  id: string
  email: string
  username: string
  display_name: string
  is_japanese: boolean
  university: string
  grade: string
  target_industry: string
  is_active: boolean
  is_admin: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Interview {
  id: string
  interview_type: string
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  target_company: string
  target_industry: string
  target_position: string
  major: string
  university: string
  duration_minutes: number
  question_count: number
  overall_score: number | null
  feedback_summary: string
  questions: InterviewQuestion[]
  started_at: string | null
  completed_at: string | null
  created_at: string
}

export interface InterviewQuestion {
  id: string
  question_text: string
  question_category: string
  order_index: number
  answer_text: string
  answer_duration_seconds: number
  has_evaluation: boolean
}

export interface InterviewStartResponse {
  interview_id: string
  question: InterviewQuestion
  total_questions: number
}

export interface Evaluation {
  id: string
  interview_question_id: string
  overall_score: number
  content_score: number
  structure_score: number
  language_score: number
  passion_score: number
  manners_score: number
  content_feedback: string
  structure_feedback: string
  language_feedback: string
  improvement_suggestions: string
  strengths: string[]
  weaknesses: string[]
  suggested_answer_points: string[]
  created_at: string
}

export interface BatchEvaluation {
  overall_score: number
  content_score: number
  structure_score: number
  language_score: number
  passion_score: number
  manners_score: number
  feedback_summary: string
  improvement_tips: string
  question_evaluations: Evaluation[]
}

/* 面接作成フォーム */
export interface InterviewFormData {
  interview_type: string
  target_company: string
  target_industry: string
  target_position: string
  major: string
  university: string
  duration_minutes: number
  question_count: number
}

/* スコア表示用 */
export interface ScoreCategory {
  label: string
  key: string
  score: number
  color: string
}
