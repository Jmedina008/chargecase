from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class PlanType(enum.Enum):
    STARTER = "starter"
    GROWTH = "growth"
    PRO = "pro"

class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Billing info
    plan = Column(Enum(PlanType), default=PlanType.STARTER)
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    
    # Connected Stripe account (their store)
    connected_stripe_account_id = Column(String, nullable=True)
    connected_stripe_user_id = Column(String, nullable=True)
    stripe_access_token = Column(Text, nullable=True)
    stripe_refresh_token = Column(Text, nullable=True)
    
    # Branding settings
    brand_name = Column(String, nullable=True)
    brand_logo_url = Column(String, nullable=True)
    sender_name = Column(String, nullable=True)
    sender_email = Column(String, nullable=True)
    
    # Settings
    dunning_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customers = relationship("Customer", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")