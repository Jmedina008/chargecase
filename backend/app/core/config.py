from pydantic_settings import BaseSettings
from typing import List
import secrets

class Settings(BaseSettings):
    # Basic app config
    APP_NAME: str = "ChargeChase"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.fly.dev"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://*.vercel.app"]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/chargechase"
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_CONNECT_CLIENT_ID: str = ""
    
    # Resend email service
    RESEND_API_KEY: str = ""
    FROM_EMAIL: str = "ChargeChase <noreply@chargechase.com>"
    
    # Stripe pricing (for our SaaS billing)
    STRIPE_STARTER_PRICE_ID: str = ""
    STRIPE_GROWTH_PRICE_ID: str = ""
    STRIPE_PRO_PRICE_ID: str = ""
    
    # Background job settings
    SCHEDULER_INTERVAL_MINUTES: int = 60
    MAX_DUNNING_ATTEMPTS: int = 4
    
    # Default dunning schedule (in hours)
    DEFAULT_DUNNING_SCHEDULE: List[int] = [0, 24, 72, 120]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()