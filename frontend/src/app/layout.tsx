import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI面接トレーナー',
  description: '日本大学生向けAI面接練習プラットフォーム',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  )
}
