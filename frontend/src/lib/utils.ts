import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const hours = Math.floor(diff / 3600000)

  if (hours < 1) return 'たった今'
  if (hours < 24) return `${hours}時間前`
  if (hours < 48) return '昨日'
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

export function scoreColor(score: number): string {
  if (score >= 85) return 'text-green-500'
  if (score >= 70) return 'text-blue-500'
  if (score >= 50) return 'text-yellow-500'
  return 'text-red-500'
}

export function scoreBgColor(score: number): string {
  if (score >= 85) return 'bg-green-500'
  if (score >= 70) return 'bg-blue-500'
  if (score >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

export function categoryLabel(cat: string): string {
  const labels: Record<string, string> = {
    self_pr: '自己PR',
    gakuchika: 'ガクチカ',
    motivation: '志望動機',
    weakness: '短所・改善',
    future: '将来像',
    reverse_q: '逆質問',
    case: 'ケース面接',
    gd: 'GD',
    general: '一般質問',
    other: 'その他',
  }
  return labels[cat] || cat
}
