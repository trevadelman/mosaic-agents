import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider } from '@/components/theme-provider'
import { Sidebar } from '@/components/sidebar/sidebar'
import { WebSocketProvider } from '@/lib/contexts/websocket-context'
import { AgentProvider } from '@/lib/contexts/agent-context'
import { ToastProvider } from '@/components/ui/toast'
import { ClerkProvider } from '@clerk/nextjs'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'MOSAIC - Multi-agent Orchestration System',
  description: 'Multi-agent Orchestration System for Adaptive Intelligent Collaboration',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <ClerkProvider>
        <body className={inter.className}>
          <ThemeProvider
            attribute="class"
            defaultTheme="dark"
            enableSystem
            disableTransitionOnChange
          >
            <WebSocketProvider>
              <AgentProvider>
                <ToastProvider>
                  <div className="flex h-screen">
                    <Sidebar />
                    <div className="flex-1 overflow-auto">
                      {children}
                    </div>
                  </div>
                </ToastProvider>
              </AgentProvider>
            </WebSocketProvider>
          </ThemeProvider>
        </body>
      </ClerkProvider>
    </html>
  )
}
