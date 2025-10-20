'use client'

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'

// Types for Whop SDK
interface WhopUser {
  id: string
  email: string
  username: string
  profile_pic_url?: string
}

interface WhopCompany {
  id: string
  name: string
  vanity_url: string
  profile_pic_url?: string
  owner_id: string
}

interface WhopExperience {
  id: string
  company_id: string
  name: string
}

interface WhopContext {
  user: WhopUser | null
  company: WhopCompany | null
  experience: WhopExperience | null
  isLoading: boolean
  error: string | null
}

const WhopContext = createContext<WhopContext>({
  user: null,
  company: null,
  experience: null,
  isLoading: true,
  error: null
})

export function WhopProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<WhopUser | null>(null)
  const [company, setCompany] = useState<WhopCompany | null>(null)
  const [experience, setExperience] = useState<WhopExperience | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    initializeWhopSDK()
  }, [])

  const initializeWhopSDK = async () => {
    try {
      // In a real implementation, this would initialize the actual Whop SDK
      // For now, we'll simulate the SDK initialization
      
      // Check if we're in an iframe (Whop environment)
      const isInWhop = window !== window.parent
      
      if (!isInWhop) {
        // Development mode - use mock data
        setUser({
          id: 'dev-user-123',
          email: 'creator@example.com',
          username: 'creator123',
          profile_pic_url: null
        })
        setCompany({
          id: 'dev-company-456',
          name: 'Test Creator Community',
          vanity_url: 'test-creator',
          profile_pic_url: null,
          owner_id: 'dev-user-123'
        })
        setExperience({
          id: 'dev-exp-789',
          company_id: 'dev-company-456',
          name: 'ChargeChase'
        })
      } else {
        // Production mode - would use actual Whop SDK
        // const whopSDK = new WhopSDK({
        //   appId: process.env.NEXT_PUBLIC_WHOP_APP_ID!,
        //   apiKey: process.env.NEXT_PUBLIC_WHOP_API_KEY!
        // })
        // 
        // const userData = await whopSDK.getUser()
        // const companyData = await whopSDK.getCompany()
        // const experienceData = await whopSDK.getExperience()
        //
        // setUser(userData)
        // setCompany(companyData)
        // setExperience(experienceData)
      }
      
      setIsLoading(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to initialize Whop SDK')
      setIsLoading(false)
    }
  }

  return (
    <WhopContext.Provider value={{
      user,
      company,
      experience,
      isLoading,
      error
    }}>
      {children}
    </WhopContext.Provider>
  )
}

// Custom hooks for using Whop context
export function useWhop() {
  const context = useContext(WhopContext)
  if (!context) {
    throw new Error('useWhop must be used within a WhopProvider')
  }
  return context
}

export function useWhopUser() {
  const { user, isLoading, error } = useWhop()
  return { user, isLoading, error }
}

export function useWhopCompany() {
  const { company, isLoading, error } = useWhop()
  return { company, isLoading, error }
}

export function useWhopExperience() {
  const { experience, isLoading, error } = useWhop()
  return { experience, isLoading, error }
}

// API helper function that includes Whop auth headers
export async function whopApiCall(endpoint: string, options: RequestInit = {}) {
  // Get auth token from localStorage or context
  const token = localStorage.getItem('whop_token') || 'dev-token-123'
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }

  // Use Whop-specific API endpoints
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const fullUrl = endpoint.startsWith('/api/') 
    ? `${baseUrl}/whop${endpoint.replace('/api/', '/companies/')}`
    : `${baseUrl}${endpoint}`

  return fetch(fullUrl, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  })
}
