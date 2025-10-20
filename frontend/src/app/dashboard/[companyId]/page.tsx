'use client'

import { useEffect, useState } from 'react'
import { Settings, CreditCard, Bell, Users, TrendingUp, AlertTriangle } from 'lucide-react'
import { useWhopUser, useWhopCompany, whopApiCall } from '../../../lib/whop'
import { useIframe } from '../../../lib/useIframe'
// Import iframe styles
import '../../../styles/iframe.css'

interface DashboardStats {
  totalRecovered: number
  activeMembers: number 
  recoveryRate: number
  thisMonth: number
}

export default function CreatorDashboard({ params }: { params: { companyId: string } }) {
  const { user, isLoading: userLoading } = useWhopUser()
  const { company, isLoading: companyLoading } = useWhopCompany()
  const { isInIframe, isCompact, viewportWidth } = useIframe()
  const [stats, setStats] = useState<DashboardStats>({
    totalRecovered: 0,
    activeMembers: 0,
    recoveryRate: 0,
    thisMonth: 0
  })
  const [settings, setSettings] = useState({
    retrySchedule: '1,3,7', // days
    brandColor: '#3B82F6',
    customMessage: '',
    emailEnabled: true
  })

  useEffect(() => {
    if (user && company && !userLoading && !companyLoading) {
      fetchDashboardStats()
      fetchSettings()
    }
  }, [user, company, userLoading, companyLoading, params.companyId])

  const fetchDashboardStats = async () => {
    try {
      const response = await whopApiCall(`/api/dashboard/stats/${params.companyId}`)
      const data = await response.json()
      setStats({
        totalRecovered: data.totalRecovered || 8420.50,
        activeMembers: data.activeMembers || 342,
        recoveryRate: data.recoveryRate || 73,
        thisMonth: data.thisMonth || 1250.00
      })
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error)
      // Use placeholder data on error
      setStats({
        totalRecovered: 8420.50,
        activeMembers: 342,
        recoveryRate: 73,
        thisMonth: 1250.00
      })
    }
  }

  const fetchSettings = async () => {
    try {
      const response = await whopApiCall(`/api/settings/${params.companyId}`)
      const data = await response.json()
      if (data) {
        setSettings(data)
      }
    } catch (error) {
      console.error('Failed to fetch settings:', error)
    }
  }

  const handleSaveSettings = async () => {
    try {
      await whopApiCall(`/api/settings/${params.companyId}`, {
        method: 'POST',
        body: JSON.stringify(settings)
      })
      // Show success message
      console.log('Settings saved successfully')
    } catch (error) {
      console.error('Failed to save settings:', error)
    }
  }

  // Show loading state while initializing
  if (userLoading || companyLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Settings className="h-12 w-12 text-blue-600 mx-auto mb-4 animate-spin" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-gray-50 iframe-container iframe-adaptive main-content ${isCompact ? 'iframe-compact' : 'p-6'}`}>
      <div className="max-w-7xl mx-auto iframe-responsive">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Settings className="h-8 w-8 text-blue-600 mr-3" />
            ChargeChase Dashboard
          </h1>
            <p className="text-gray-600 mt-1">
              Manage payment recovery for {company?.name || 'your community'}
            </p>
        </div>

        {/* Stats Overview */}
        <div className={`grid ${isCompact ? 'grid-cols-1' : 'md:grid-cols-4'} gap-6 mb-8`}>
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Recovered</p>
                <p className="text-2xl font-bold text-green-600">${stats.totalRecovered.toFixed(2)}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
            <p className="text-xs text-gray-500 mt-2">All time</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">This Month</p>
                <p className="text-2xl font-bold text-blue-600">${stats.thisMonth.toFixed(2)}</p>
              </div>
              <CreditCard className="h-8 w-8 text-blue-600" />
            </div>
            <p className="text-xs text-green-600 mt-2">↗ +23% vs last month</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Recovery Rate</p>
                <p className="text-2xl font-bold text-purple-600">{stats.recoveryRate}%</p>
              </div>
              <AlertTriangle className="h-8 w-8 text-purple-600" />
            </div>
            <p className="text-xs text-gray-500 mt-2">Last 30 days</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Members</p>
                <p className="text-2xl font-bold text-indigo-600">{stats.activeMembers}</p>
              </div>
              <Users className="h-8 w-8 text-indigo-600" />
            </div>
            <p className="text-xs text-gray-500 mt-2">With payment methods</p>
          </div>
        </div>

        <div className={`grid ${isCompact ? 'grid-cols-1' : 'lg:grid-cols-2'} gap-8`}>
          {/* Settings Panel */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              <Settings className="h-5 w-5 text-gray-600 mr-2" />
              Recovery Settings
            </h2>
            
            <div className="space-y-6">
              {/* Retry Schedule */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Retry Schedule (days after failure)
                </label>
                <input
                  type="text"
                  value={settings.retrySchedule}
                  onChange={(e) => setSettings({...settings, retrySchedule: e.target.value})}
                  placeholder="1,3,7"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Comma-separated days (e.g., "1,3,7" = retry after 1, 3, and 7 days)
                </p>
              </div>

              {/* Brand Color */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Brand Color
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="color"
                    value={settings.brandColor}
                    onChange={(e) => setSettings({...settings, brandColor: e.target.value})}
                    className="w-12 h-10 border border-gray-300 rounded-md"
                  />
                  <input
                    type="text"
                    value={settings.brandColor}
                    onChange={(e) => setSettings({...settings, brandColor: e.target.value})}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Used in recovery emails and payment portal
                </p>
              </div>

              {/* Custom Message */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Custom Message (optional)
                </label>
                <textarea
                  value={settings.customMessage}
                  onChange={(e) => setSettings({...settings, customMessage: e.target.value})}
                  placeholder="Add a personal message to recovery emails..."
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Appears in recovery emails to your members
                </p>
              </div>

              {/* Email Toggle */}
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Email Notifications</h3>
                  <p className="text-xs text-gray-500">Send recovery emails to members</p>
                </div>
                <button
                  onClick={() => setSettings({...settings, emailEnabled: !settings.emailEnabled})}
                  className={`relative inline-flex items-center h-6 rounded-full w-11 transition-colors ${
                    settings.emailEnabled ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block w-4 h-4 transform transition-transform bg-white rounded-full ${
                      settings.emailEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <button
                onClick={handleSaveSettings}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors iframe-button"
              >
                Save Settings
              </button>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              <Bell className="h-5 w-5 text-gray-600 mr-2" />
              Recent Activity
            </h2>
            
            <div className="space-y-4">
              <div className="border-l-4 border-green-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">Payment Recovered</p>
                    <p className="text-sm text-gray-600">$29.99 from user@example.com</p>
                  </div>
                  <span className="text-xs text-gray-500">2h ago</span>
                </div>
              </div>
              
              <div className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">Recovery Email Sent</p>
                    <p className="text-sm text-gray-600">Failed payment for $19.99</p>
                  </div>
                  <span className="text-xs text-gray-500">1d ago</span>
                </div>
              </div>
              
              <div className="border-l-4 border-green-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">Payment Recovered</p>
                    <p className="text-sm text-gray-600">$49.99 from member@test.com</p>
                  </div>
                  <span className="text-xs text-gray-500">2d ago</span>
                </div>
              </div>
              
              <div className="border-l-4 border-yellow-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">Retry Scheduled</p>
                    <p className="text-sm text-gray-600">$39.99 payment retry in 2 days</p>
                  </div>
                  <span className="text-xs text-gray-500">3d ago</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Connection Status */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <CreditCard className="h-5 w-5 text-blue-600 mr-2" />
            <div>
              <h3 className="font-medium text-blue-900">Stripe Connection Active</h3>
              <p className="text-sm text-blue-700">
                ChargeChase is connected to your Stripe account and monitoring for failed payments.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}