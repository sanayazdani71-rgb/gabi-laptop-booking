import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '30-Day Glow-Up — Life Design Template',
  description: 'A ready-made system for your body, habits, and confidence. Stop planning to start. Just fill it in.',
  openGraph: {
    title: '30-Day Glow-Up — Life Design Template',
    description: 'A ready-made system for your body, habits, and confidence.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
