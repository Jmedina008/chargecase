# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

ChargeChase is an automated failed payment recovery service built with a FastAPI backend and Next.js frontend. The application helps businesses recover lost revenue by sending branded dunning messages with secure billing portal links when payments fail.

## Tech Stack

**Backend**: FastAPI + PostgreSQL + SQLAlchemy + Alembic
**Frontend**: Next.js 14 + TypeScript + Tailwind CSS
**Integrations**: Stripe (payments & Connect), Resend (email)

## Development Commands

### Backend (FastAPI)

Start development server:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run with Python directly:
```bash
cd backend
python -m app.main
```

Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Database migrations:
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend (Next.js)

Development server:
```bash
cd frontend
npm run dev
```

Build and start production:
```bash
cd frontend
npm run build
npm run start
```

Type checking:
```bash
cd frontend
npm run type-check
```

Linting:
```bash
cd frontend
npm run lint
```

Install dependencies:
```bash
cd frontend
npm install
```

## Architecture

### Backend Structure

- **`app/main.py`**: FastAPI application entry point with middleware, CORS, and route registration
- **`app/core/`**: Configuration, database setup, and core utilities
- **`app/models/`**: SQLAlchemy database models (User, Customer, etc.)
- **`app/api/routes/`**: API route handlers organized by feature (auth, webhooks, dashboard, onboarding)
- **`app/schemas/`**: Pydantic models for request/response validation
- **`app/services/`**: Business logic and external service integrations
- **`app/workers/`**: Background job processing

### Frontend Structure

- **`src/app/`**: Next.js 14 App Router pages and layouts
- **`src/components/`**: Reusable React components
- **`src/lib/`**: Utility functions and shared logic
- **`src/types/`**: TypeScript type definitions

### Key Features

1. **Stripe Integration**: Dual Stripe integration - one for ChargeChase's own billing, another for connected accounts (customers' Stripe accounts)
2. **Webhook Processing**: Handles Stripe webhooks for failed payments and triggers dunning sequences
3. **Dunning Management**: Configurable retry schedules and branded email campaigns
4. **Dashboard**: Revenue recovery tracking and analytics
5. **Onboarding**: Stripe Connect integration for customer account linking

### Database Models

- **User**: ChargeChase account holders with subscription management
- **Customer**: End customers whose payments failed (belongs to a User)
- **Event**: Audit log of dunning events and payment recovery attempts
- **Settings**: User-specific configuration for dunning campaigns

## Environment Variables

Required environment variables for local development:

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `STRIPE_SECRET_KEY`: Stripe secret key for ChargeChase billing
- `STRIPE_WEBHOOK_SECRET`: Webhook endpoint secret
- `STRIPE_CONNECT_CLIENT_ID`: For Stripe Connect integration
- `RESEND_API_KEY`: Email service API key

## Testing

No test framework is currently configured. When adding tests, use pytest for backend and Jest/React Testing Library for frontend.

## Database

Uses PostgreSQL with SQLAlchemy ORM and Alembic for migrations. Database tables are created automatically on startup via `create_tables()` in the lifespan manager.

## Logging

Backend uses structured logging with `structlog` configured for JSON output. All requests are automatically logged with method, path, and response status.

## Development Notes

- The backend serves as both the API for the frontend and handles Stripe webhooks
- Frontend uses Tailwind CSS with custom button classes (`.btn-primary`)
- Stripe Connect is used to access customer Stripe accounts for webhook processing
- Email templates should maintain brand consistency with user-configured branding settings