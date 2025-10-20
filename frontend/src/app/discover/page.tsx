'use client'

import { CreditCard, TrendingUp, Shield, Zap, CheckCircle, DollarSign } from 'lucide-react'

export default function ChargeChaseDiscover() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center mb-6">
            <CreditCard className="h-16 w-16 text-blue-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Stop Losing Revenue to Failed Payments
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            ChargeChase automatically recovers failed payments from your community members 
            with branded dunning messages and secure billing portal integration.
          </p>
          
          {/* Pricing Badge */}
          <div className="inline-flex items-center bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-medium mb-8">
            <DollarSign className="h-4 w-4 mr-1" />
            Only 2.9% fee on recovered revenue • No monthly costs
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">78%</div>
              <div className="text-gray-600">Average Recovery Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600 mb-2">$2.4M+</div>
              <div className="text-gray-600">Revenue Recovered</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-600 mb-2">< 2 min</div>
              <div className="text-gray-600">Setup Time</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Creators Choose ChargeChase
            </h2>
            <p className="text-lg text-gray-600">
              Purpose-built for digital creators and community owners
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="bg-blue-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Instant Setup</h3>
              <p className="text-gray-600">
                Connect your Stripe account and start recovering payments immediately. No complex configuration required.
              </p>
            </div>
            
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="bg-green-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">PCI Compliant</h3>
              <p className="text-gray-600">
                All card updates happen in Stripe's secure billing portal. We never store or see payment data.
              </p>
            </div>
            
            <div className="bg-white rounded-lg p-6 shadow-sm">
              <div className="bg-purple-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Smart Analytics</h3>
              <p className="text-gray-600">
                Track recovered revenue, conversion rates, and member retention metrics in real-time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How ChargeChase Works
            </h2>
            <p className="text-lg text-gray-600">
              Fully automated payment recovery in 4 simple steps
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-red-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-red-600 font-bold text-lg">1</span>
              </div>
              <h3 className="font-semibold mb-2 text-gray-900">Payment Fails</h3>
              <p className="text-sm text-gray-600">
                Stripe detects a failed payment and sends us a secure webhook notification
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-blue-600 font-bold text-lg">2</span>
              </div>
              <h3 className="font-semibold mb-2 text-gray-900">Send Recovery Email</h3>
              <p className="text-sm text-gray-600">
                We send a branded email with your community's design and secure portal link
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-green-600 font-bold text-lg">3</span>
              </div>
              <h3 className="font-semibold mb-2 text-gray-900">Member Updates</h3>
              <p className="text-sm text-gray-600">
                Member clicks link and securely updates their payment method in Stripe
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <span className="text-purple-600 font-bold text-lg">4</span>
              </div>
              <h3 className="font-semibold mb-2 text-gray-900">Revenue Recovered</h3>
              <p className="text-sm text-gray-600">
                Payment is retried automatically and your revenue is recovered
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-16 bg-blue-600">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Join 500+ Creators Already Recovering Revenue
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            "ChargeChase recovered $3,200 in the first month. It pays for itself instantly."
          </p>
          <div className="text-blue-200">
            <p className="font-medium">Sarah Chen</p>
            <p className="text-sm">Creator, SaaS Academy (2,400 members)</p>
          </div>
        </div>
      </section>

      {/* Features List */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Everything You Need to Recover Revenue
            </h2>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            {[
              'Automated dunning sequences',
              'Branded recovery emails',
              'Secure Stripe integration', 
              'Real-time analytics dashboard',
              'Member retention tracking',
              'Custom retry schedules',
              'Mobile-optimized portal',
              'Webhook health monitoring'
            ].map((feature, index) => (
              <div key={index} className="flex items-center">
                <CheckCircle className="h-5 w-5 text-green-600 mr-3 flex-shrink-0" />
                <span className="text-gray-700">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-white">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Stop Losing Revenue?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Install ChargeChase in your community and start recovering failed payments today.
          </p>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <p className="text-green-800 font-medium">
              💰 Only pay when we recover your revenue: 2.9% fee on successful recoveries
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}