import type { Metadata } from 'next'
import './globals.css'
import { WhopProvider } from '../lib/whop'

export const metadata: Metadata = {
  title: 'ChargeChase - Recover Failed Payments Automatically',
  description: 'Recover failed payments automatically with branded dunning messages and secure billing portal integration.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <WhopProvider>
          {children}
        </WhopProvider>
      </body>
    </html>
  )
}
