from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class RecoveryStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RECOVERED = "recovered"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WhopCustomer(Base):
    """
    Represents a customer whose payments have failed (scoped by Whop company)
    """
    __tablename__ = "whop_customers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("whop_companies.id"), nullable=False, index=True)
    
    # Stripe customer info (from their connected account)
    stripe_customer_id = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    name = Column(String, nullable=True)
    
    # Recovery status
    recovery_status = Column(Enum(RecoveryStatus), default=RecoveryStatus.PENDING)
    total_failed_amount = Column(Integer, default=0)  # In cents
    total_recovered_amount = Column(Integer, default=0)  # In cents
    
    # Recovery settings
    dont_email = Column(Boolean, default=False)  # Flag if hard bounced or unsubscribed
    
    # Last activity
    last_failed_payment_at = Column(DateTime(timezone=True), nullable=True)
    last_recovery_email_sent_at = Column(DateTime(timezone=True), nullable=True)
    last_recovered_payment_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("WhopCompany", back_populates="customers")
    recovery_events = relationship("RecoveryEvent", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<WhopCustomer(email='{self.email}', status='{self.recovery_status}')>"


class RecoveryEvent(Base):
    """
    Represents an event in the payment recovery process
    """
    __tablename__ = "recovery_events"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("whop_companies.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("whop_customers.id"), nullable=False, index=True)
    
    # Event details
    event_type = Column(String, nullable=False, index=True)  # 'payment_failed', 'email_sent', 'payment_recovered', etc.
    stripe_event_id = Column(String, nullable=True, index=True)
    stripe_invoice_id = Column(String, nullable=True, index=True)
    
    # Amount information
    amount = Column(Integer, nullable=False)  # In cents
    currency = Column(String, default="usd")
    
    # Recovery attempt info
    retry_attempt = Column(Integer, default=1)
    recovery_email_sent = Column(Boolean, default=False)
    
    # Metadata
    metadata = Column(Text, nullable=True)  # JSON string for additional data
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    stripe_created_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    company = relationship("WhopCompany", back_populates="recovery_events")
    customer = relationship("WhopCustomer", back_populates="recovery_events")
    
    def __repr__(self):
        return f"<RecoveryEvent(event_type='{self.event_type}', amount={self.amount})>"