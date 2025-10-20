from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class WhopCompany(Base):
    """
    Represents a Whop company/community that has installed ChargeChase
    """
    __tablename__ = "whop_companies"

    id = Column(Integer, primary_key=True, index=True)
    
    # Whop-specific IDs
    whop_company_id = Column(String, unique=True, index=True, nullable=False)
    whop_owner_id = Column(String, nullable=False, index=True)
    
    # Company info from Whop
    name = Column(String, nullable=False)
    vanity_url = Column(String, nullable=True)
    profile_pic_url = Column(String, nullable=True)
    
    # ChargeChase-specific settings
    is_active = Column(Boolean, default=True)
    
    # Connected Stripe account (their store)
    connected_stripe_account_id = Column(String, nullable=True)
    connected_stripe_user_id = Column(String, nullable=True)
    stripe_access_token = Column(Text, nullable=True)
    stripe_refresh_token = Column(Text, nullable=True)
    stripe_connected_at = Column(DateTime(timezone=True), nullable=True)
    
    # Branding settings
    brand_color = Column(String, default="#3B82F6")
    custom_message = Column(Text, nullable=True)
    sender_name = Column(String, nullable=True)
    sender_email = Column(String, nullable=True)
    
    # Recovery settings
    dunning_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    retry_schedule = Column(String, default="1,3,7")  # Days after failure
    
    # App installation info
    app_installed_at = Column(DateTime(timezone=True), server_default=func.now())
    last_webhook_at = Column(DateTime(timezone=True), nullable=True)
    
    # Revenue tracking (for transaction fees)
    total_recovered = Column(Integer, default=0)  # In cents
    total_fees_owed = Column(Integer, default=0)  # In cents (2.9% of recovered)
    total_fees_paid = Column(Integer, default=0)  # In cents
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customers = relationship("WhopCustomer", back_populates="company", cascade="all, delete-orphan")
    recovery_events = relationship("RecoveryEvent", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<WhopCompany(whop_company_id='{self.whop_company_id}', name='{self.name}')>"


class WhopUser(Base):
    """
    Represents a Whop user (for caching user info, not authentication)
    """
    __tablename__ = "whop_users"
    
    id = Column(Integer, primary_key=True, index=True)
    whop_user_id = Column(String, unique=True, index=True, nullable=False)
    
    # User info from Whop
    email = Column(String, nullable=True)
    username = Column(String, nullable=True)
    profile_pic_url = Column(String, nullable=True)
    
    # Cache timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<WhopUser(whop_user_id='{self.whop_user_id}', username='{self.username}')>"