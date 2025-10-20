'use client'

import { useState } from 'react'
import { Monitor, Smartphone, Tablet } from 'lucide-react'

export default function TestEmbed() {
  const [viewportSize, setViewportSize] = useState('desktop')
  const [theme, setTheme] = useState('light')
  
  const getIframeSize = () => {
    switch (viewportSize) {
      case 'mobile':
        return { width: '375px', height: '667px' }
      case 'tablet':
        return { width: '768px', height: '1024px' }
      default:
        return { width: '1200px', height: '800px' }
    }
  }

  const { width, height } = getIframeSize()

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            ChargeChase Whop App Test Environment
          </h1>
          <p className="text-gray-600 mb-6">
            Test the ChargeChase app as it would appear when embedded in a Whop community.
          </p>

          {/* Test Controls */}
          <div className="flex flex-wrap gap-4 mb-6 p-4 bg-white rounded-lg shadow-sm">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">Viewport:</span>
              <button
                onClick={() => setViewportSize('desktop')}
                className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
                  viewportSize === 'desktop' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                <Monitor className="h-4 w-4" />
                Desktop
              </button>
              <button
                onClick={() => setViewportSize('tablet')}
                className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
                  viewportSize === 'tablet' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                <Tablet className="h-4 w-4" />
                Tablet
              </button>
              <button
                onClick={() => setViewportSize('mobile')}
                className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
                  viewportSize === 'mobile' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                <Smartphone className="h-4 w-4" />
                Mobile
              </button>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">Theme:</span>
              <button
                onClick={() => setTheme('light')}
                className={`px-3 py-1 rounded text-sm ${
                  theme === 'light' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Light
              </button>
              <button
                onClick={() => setTheme('dark')}
                className={`px-3 py-1 rounded text-sm ${
                  theme === 'dark' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                }`}
              >
                Dark
              </button>
            </div>
          </div>
        </div>

        {/* Test Scenarios */}
        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900">Test Pages</h2>
            
            <div className="space-y-2">
              <a
                href={`/experiences/test-exp-123?theme=${theme}`}
                target="test-frame"
                className="block p-3 bg-white rounded border hover:bg-blue-50 transition-colors"
              >
                <div className="font-medium text-blue-600">Experience Page</div>
                <div className="text-sm text-gray-600">Main app interface for community members</div>
              </a>
              
              <a
                href={`/dashboard/test-company-456?theme=${theme}`}
                target="test-frame"
                className="block p-3 bg-white rounded border hover:bg-blue-50 transition-colors"
              >
                <div className="font-medium text-blue-600">Creator Dashboard</div>
                <div className="text-sm text-gray-600">Management dashboard for creators</div>
              </a>
              
              <a
                href={`/discover?theme=${theme}`}
                target="test-frame"
                className="block p-3 bg-white rounded border hover:bg-blue-50 transition-colors"
              >
                <div className="font-medium text-blue-600">Discover Page</div>
                <div className="text-sm text-gray-600">App store listing page</div>
              </a>
            </div>
          </div>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900">Test Scenarios</h2>
            
            <div className="space-y-2">
              <div className="p-3 bg-white rounded border">
                <div className="font-medium text-gray-900">✅ Iframe Detection</div>
                <div className="text-sm text-gray-600">App should detect it's in an iframe</div>
              </div>
              
              <div className="p-3 bg-white rounded border">
                <div className="font-medium text-gray-900">✅ Responsive Layout</div>
                <div className="text-sm text-gray-600">Layout should adapt to iframe size</div>
              </div>
              
              <div className="p-3 bg-white rounded border">
                <div className="font-medium text-gray-900">✅ No Scrollbars</div>
                <div className="text-sm text-gray-600">Content should fit without scrolling issues</div>
              </div>
              
              <div className="p-3 bg-white rounded border">
                <div className="font-medium text-gray-900">✅ Interactive Elements</div>
                <div className="text-sm text-gray-600">Buttons and forms should work properly</div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-gray-900">Debug Info</h2>
            
            <div className="p-4 bg-white rounded border text-sm space-y-2">
              <div><strong>Iframe Size:</strong> {width} × {height}</div>
              <div><strong>Theme:</strong> {theme}</div>
              <div><strong>Viewport:</strong> {viewportSize}</div>
            </div>
            
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
              <div className="font-medium text-yellow-800 mb-1">Note</div>
              <div className="text-sm text-yellow-700">
                This simulates how the app will appear when embedded in Whop communities. 
                Test different viewport sizes and themes to ensure compatibility.
              </div>
            </div>
          </div>
        </div>

        {/* Iframe Container */}
        <div className="bg-white rounded-lg shadow-lg p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Embedded App Preview ({viewportSize})
            </h2>
            <div className="text-sm text-gray-600">
              {width} × {height}
            </div>
          </div>
          
          <div className="border border-gray-300 rounded-lg overflow-hidden bg-gray-50 flex items-center justify-center" style={{ height: height }}>
            <iframe
              name="test-frame"
              src="/experiences/test-exp-123"
              style={{ 
                width: width, 
                height: height,
                border: 'none',
                borderRadius: '8px'
              }}
              title="ChargeChase App Test"
            />
          </div>
          
          <div className="mt-4 text-xs text-gray-500">
            💡 Click the test page links above to load different pages in the iframe
          </div>
        </div>

        {/* Developer Notes */}
        <div className="mt-8 p-6 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">Developer Testing Checklist</h3>
          <div className="text-sm text-blue-800 space-y-1">
            <div>• Verify iframe detection works (check browser console)</div>
            <div>• Test responsive behavior across all viewport sizes</div>
            <div>• Ensure no horizontal scrollbars appear</div>
            <div>• Validate that PostMessage communication works</div>
            <div>• Check theme switching functionality</div>
            <div>• Test all interactive elements (buttons, forms, dropdowns)</div>
            <div>• Verify loading states appear correctly</div>
            <div>• Check that external links handle iframe context properly</div>
          </div>
        </div>
      </div>
    </div>
  )
}