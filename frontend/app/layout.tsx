import type { Metadata } from 'next'
import { Manrope, Space_Grotesk } from 'next/font/google'

import './globals.css'

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-manrope',
})

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
})

export const metadata: Metadata = {
  title: 'Podcast Buddy',
  description: 'AI-powered news-to-podcast studio for premium editorial briefings.',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${manrope.variable} ${spaceGrotesk.variable} bg-bg text-text antialiased`}>
        {children}
      </body>
    </html>
  )
}