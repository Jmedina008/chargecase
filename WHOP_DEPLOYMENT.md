# ChargeChase Whop App Deployment Guide

## 🎯 Overview

ChargeChase has been successfully converted from a standalone SaaS application to a **Whop App** that can be installed and used by Whop creators in their communities.

### Key Features
- **Transaction Fee Model**: 2.9% fee on recovered revenue
- **Multi-tenant Architecture**: Each Whop community operates independently
- **Iframe Optimized**: Fully responsive and embedded-friendly UI
- **Automatic Payment Recovery**: Integrates with creators' Stripe accounts

---

## 🏗️ Architecture Changes

### Frontend Changes
```
Original Structure → Whop App Structure
├── /page.tsx              ├── /experiences/[experienceId]/page.tsx  (Main app)
├── /login                  ├── /dashboard/[companyId]/page.tsx      (Creator settings)
├── /dashboard             ├── /discover/page.tsx                   (App store listing)
└── /pricing               └── /test-embed/page.tsx                 (Testing)
```

### Backend Changes
- **New Models**: `WhopCompany`, `WhopUser`, `WhopCustomer`, `RecoveryEvent`
- **Whop Authentication**: JWT tokens from Whop instead of custom auth
- **Multi-tenancy**: All data scoped by `whop_company_id`
- **Payment Integration**: Transaction fees processed through Whop's payment system

---

## 🚀 Deployment Steps

### 1. Environment Setup

Create `.env.local` in the frontend directory:

```bash
# Whop App Configuration
NEXT_PUBLIC_WHOP_APP_ID=your_whop_app_id_here
NEXT_PUBLIC_WHOP_API_KEY=your_whop_api_key_here
WHOP_WEBHOOK_SECRET=your_whop_webhook_secret_here

# Backend API
NEXT_PUBLIC_API_URL=https://your-backend-api.com
API_SECRET_KEY=your_api_secret_key_here

# Existing Stripe Configuration (for payment recovery functionality)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret_here
STRIPE_CONNECT_CLIENT_ID=ca_your_stripe_connect_client_id_here

# Email Service
RESEND_API_KEY=re_your_resend_api_key_here

# Database
DATABASE_URL=postgresql://user:password@host:5432/chargechase
```

### 2. Whop Developer Dashboard Setup

1. **Create Whop App**:
   - Go to [Whop Developer Dashboard](https://dev.whop.com)
   - Create a new app named "ChargeChase"
   - Set app type to "Embedded App"

2. **Configure App Paths**:
   - **Base URL**: `https://your-domain.vercel.app`
   - **App Path**: `/experiences/[experienceId]`
   - **Dashboard Path**: `/dashboard/[companyId]`
   - **Discover Path**: `/discover`

3. **Set Pricing Model**:
   - Type: Transaction Fee
   - Percentage: 2.9%
   - Description: "Fee charged on successfully recovered payments"

4. **Configure Webhooks**:
   - App Installation: `https://your-backend-api.com/whop/webhooks/whop`
   - Payment Events: `https://your-backend-api.com/whop/webhooks/whop`

### 3. Backend Deployment

1. **Update Dependencies**:
   ```bash
   pip install fastapi sqlalchemy alembic psycopg2-binary requests python-multipart
   ```

2. **Database Migration**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add Whop models"
   alembic upgrade head
   ```

3. **Deploy to Production**:
   - Railway, Render, or AWS
   - Ensure `/whop/` API endpoints are accessible
   - Configure CORS for your frontend domain

### 4. Frontend Deployment

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Build and Deploy**:
   ```bash
   npm run build
   ```

3. **Deploy to Vercel**:
   ```bash
   npm i -g vercel
   vercel --prod
   ```

   Or use GitHub integration for automatic deployments.

---

## 🧪 Testing

### Local Testing

1. **Start Backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Iframe Embedding**:
   Visit `http://localhost:3000/test-embed` to test the app in various iframe configurations.

### Testing Checklist

- [ ] **Iframe Detection**: App correctly identifies when embedded
- [ ] **Responsive Design**: Works across desktop, tablet, and mobile iframe sizes
- [ ] **Authentication**: Whop SDK integration functions properly
- [ ] **API Calls**: All endpoints work with Whop authentication headers
- [ ] **Payment Integration**: Transaction fees are calculated and processed
- [ ] **Webhooks**: Stripe and Whop webhooks are received and processed
- [ ] **Multi-tenancy**: Data is properly scoped by company

### Production Testing

1. **Create Test Community**: Set up a Whop community for testing
2. **Install App**: Install ChargeChase from the Whop app store
3. **Connect Stripe**: Test the Stripe Connect flow
4. **Simulate Payment Failure**: Create test scenarios with failed payments
5. **Verify Recovery**: Confirm that dunning emails are sent and payments recovered
6. **Check Billing**: Ensure transaction fees are properly charged

---

## 📊 Monitoring & Analytics

### Key Metrics to Track
- **Installation Rate**: Number of communities installing the app
- **Connection Rate**: Percentage of installs that connect Stripe accounts
- **Recovery Rate**: Percentage of failed payments successfully recovered
- **Revenue**: Total transaction fees collected
- **Churn**: Communities that uninstall the app

### Logging
- All API requests are logged with Whop company context
- Payment recovery events are tracked in `RecoveryEvent` model
- Transaction fees are logged for accounting purposes

---

## 🔧 Maintenance

### Regular Tasks
1. **Monitor Webhook Health**: Ensure Stripe and Whop webhooks are processing
2. **Process Batch Fees**: Run monthly billing for accumulated transaction fees
3. **Update Dependencies**: Keep Whop SDK and other packages updated
4. **Review Analytics**: Monitor app performance and user engagement

### Scaling Considerations
- **Database**: Consider read replicas for high-traffic communities
- **Background Jobs**: Implement Redis/Celery for processing dunning sequences
- **CDN**: Use CloudFront or similar for static assets
- **Monitoring**: Set up alerts for failed payments, webhook issues, etc.

---

## 📋 Troubleshooting

### Common Issues

**App Not Loading in Iframe**:
- Check CORS settings in backend
- Verify iframe-safe CSS classes are applied
- Ensure no fixed positioning elements

**Authentication Errors**:
- Verify Whop app ID and API keys
- Check token format in API calls
- Confirm webhook signatures are valid

**Payment Processing Issues**:
- Verify Stripe Connect permissions
- Check webhook endpoint accessibility
- Monitor transaction fee calculations

**Database Connection Issues**:
- Confirm DATABASE_URL is correct
- Check database connection limits
- Verify migrations are applied

### Support Resources
- [Whop Developer Documentation](https://dev.whop.com/docs)
- [Stripe Connect Documentation](https://stripe.com/docs/connect)
- [ChargeChase Support](mailto:support@chargechase.com)

---

## 🎉 Launch Checklist

- [ ] Environment variables configured
- [ ] Whop app created and configured
- [ ] Backend deployed with all endpoints working
- [ ] Frontend deployed and accessible
- [ ] Database migrations applied
- [ ] Webhooks configured and tested
- [ ] Payment processing tested
- [ ] App submitted to Whop app store
- [ ] Documentation updated
- [ ] Monitoring and alerts configured

**Congratulations! ChargeChase is now ready to help Whop creators recover failed payments and grow their revenue.** 🚀