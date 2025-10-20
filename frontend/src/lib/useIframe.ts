import { useEffect, useState } from 'react'

interface IframeInfo {
  isInIframe: boolean
  parentOrigin: string | null
  viewportWidth: number
  viewportHeight: number
  isCompact: boolean
}

export function useIframe(): IframeInfo {
  const [iframeInfo, setIframeInfo] = useState<IframeInfo>({
    isInIframe: false,
    parentOrigin: null,
    viewportWidth: typeof window !== 'undefined' ? window.innerWidth : 1200,
    viewportHeight: typeof window !== 'undefined' ? window.innerHeight : 800,
    isCompact: false
  })

  useEffect(() => {
    if (typeof window === 'undefined') return

    const checkIframeStatus = () => {
      const isInIframe = window !== window.parent
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight
      const isCompact = viewportWidth < 768 || viewportHeight < 600

      let parentOrigin = null
      if (isInIframe) {
        try {
          parentOrigin = document.referrer ? new URL(document.referrer).origin : null
        } catch (e) {
          // If we can't get referrer, try to get it from postMessage
          parentOrigin = 'unknown'
        }
      }

      setIframeInfo({
        isInIframe,
        parentOrigin,
        viewportWidth,
        viewportHeight,
        isCompact
      })

      // Apply iframe-specific classes to body
      if (isInIframe) {
        document.body.classList.add('iframe-body')
        document.documentElement.classList.add('iframe-container')
        
        if (isCompact) {
          document.body.classList.add('iframe-compact')
        }
      }
    }

    // Check on mount
    checkIframeStatus()

    // Listen for resize events
    window.addEventListener('resize', checkIframeStatus)

    // Set up postMessage communication with parent
    const handleMessage = (event: MessageEvent) => {
      // Validate origin if we know the parent
      if (iframeInfo.parentOrigin && event.origin !== iframeInfo.parentOrigin) {
        return
      }

      // Handle messages from parent (Whop)
      switch (event.data.type) {
        case 'THEME_CHANGE':
          // Handle theme changes from parent
          document.body.setAttribute('data-theme', event.data.theme)
          break
        case 'RESIZE':
          // Handle resize notifications
          checkIframeStatus()
          break
        case 'FOCUS':
          // Handle focus events
          if (event.data.focused) {
            // App is now visible
          } else {
            // App is now hidden
          }
          break
      }
    }

    window.addEventListener('message', handleMessage)

    return () => {
      window.removeEventListener('resize', checkIframeStatus)
      window.removeEventListener('message', handleMessage)
    }
  }, [])

  return iframeInfo
}

// Helper function to send messages to parent
export function sendToParent(message: any) {
  if (typeof window === 'undefined' || window === window.parent) {
    return // Not in iframe
  }

  try {
    window.parent.postMessage(message, '*')
  } catch (e) {
    console.warn('Failed to send message to parent:', e)
  }
}

// Helper function to handle navigation in iframe context
export function navigateInIframe(url: string) {
  if (typeof window === 'undefined') return

  if (window !== window.parent) {
    // In iframe - request parent to navigate
    sendToParent({
      type: 'NAVIGATE',
      url: url
    })
  } else {
    // Not in iframe - normal navigation
    window.location.href = url
  }
}

// Helper function to optimize scroll behavior in iframe
export function useIframeScroll() {
  useEffect(() => {
    if (typeof window === 'undefined') return

    const isInIframe = window !== window.parent
    if (!isInIframe) return

    // Prevent body scroll in iframe to avoid double scrollbars
    const handleScroll = (e: Event) => {
      e.preventDefault()
      
      // Instead of scrolling body, scroll the main content area
      const mainContent = document.querySelector('.main-content')
      if (mainContent) {
        mainContent.scrollTop += (e as any).deltaY
      }
    }

    // Add passive: false to allow preventDefault
    document.addEventListener('wheel', handleScroll, { passive: false })

    return () => {
      document.removeEventListener('wheel', handleScroll)
    }
  }, [])
}

// Helper to detect if we're in Whop specifically
export function useWhopIframe() {
  const { isInIframe, parentOrigin } = useIframe()
  
  const isInWhop = isInIframe && (
    parentOrigin?.includes('whop.com') || 
    parentOrigin?.includes('whop.dev') ||
    // For development
    parentOrigin?.includes('localhost')
  )

  return {
    isInIframe,
    isInWhop,
    parentOrigin
  }
}