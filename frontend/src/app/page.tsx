'use client'

import { CreditCard, TrendingUp, Shield, Zap } from 'lucide-react'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <CreditCard className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">ChargeChase</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-600 hover:text-gray-900">
                Login
              </Link>
              <Link href="/pricing" className="btn-primary">
                Start Recovering
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Recover Failed Payments
              <span className="text-blue-600"> Automatically</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Stop losing revenue to failed payments. ChargeChase sends branded dunning messages 
              with secure billing portal links to recover your revenue automatically.
            </p>
            <div className="flex justify-center space-x-4">
              <Link href="/pricing" className="btn-primary text-lg px-8 py-3">
                Start Recovering Payments
              </Link>
            </div>
            <p className="text-sm text-gray-500 mt-4">
              No free trial • 30-day money-back guarantee
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose ChargeChase?
            </h2>
            <p className="text-lg text-gray-600">
              Built specifically for creators selling digital products and memberships
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">2-Minute Setup</h3>
              <p className="text-gray-600">
                Connect Stripe, choose your cadence, and go live. Minimal time to value.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <Shield className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">PCI Compliant</h3>
              <p className="text-gray-600">
                All card updates happen in Stripe Billing Portal. No card data stored.
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Track Recovery</h3>
              <p className="text-gray-600">
                Monitor recovered revenue, conversion rates, and time-to-recovery metrics.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-red-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <span className="text-red-600 font-bold">1</span>
              </div>
              <h3 className="font-semibold mb-2">Payment Fails</h3>
              <p className="text-sm text-gray-600">
                Stripe detects a failed payment and sends us a webhook
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <span className="text-blue-600 font-bold">2</span>
              </div>
              <h3 className="font-semibold mb-2">Send Message</h3>
              <p className="text-sm text-gray-600">
                We send a branded email with secure billing portal link
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <span className="text-green-600 font-bold">3</span>
              </div>
              <h3 className="font-semibold mb-2">Customer Updates</h3>
              <p className="text-sm text-gray-600">
                Customer clicks link and updates payment method securely
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 rounded-full p-3 w-12 h-12 mx-auto mb-4">
                <span className="text-purple-600 font-bold">4</span>
              </div>
              <h3 className="font-semibold mb-2">Payment Recovered</h3>
              <p className="text-sm text-gray-600">
                We retry the payment and track your recovered revenue
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing CTA */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Stop Losing Revenue?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join creators who are recovering thousands in failed payments
          </p>
          <Link href="/pricing" className="bg-white text-blue-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-lg text-lg transition-colors">
            View Pricing & Start Now
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <CreditCard className="h-6 w-6 text-blue-400" />
              <span className="ml-2 text-lg font-bold">ChargeChase</span>
            </div>
            <div className="text-sm text-gray-400">
              © 2024 ChargeChase. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}