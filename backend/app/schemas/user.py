from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field, validator
from datetime import datetime
from app.models.user import PlanType, SubscriptionStatus
import re

# Base user schema
class UserBase(BaseModel):
    email: EmailStr

# Schema for user creation (registration)
class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters"
    )
    
    # Optional fields for onboarding
    brand_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Brand name (1-100 characters)"
    )
    sender_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Sender name (1-100 characters)"
    )
    sender_email: Optional[EmailStr] = Field(
        None,
        description="Valid email address for sender"
    )
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if len(v) > 128:
            raise ValueError('Password must be no more than 128 characters long')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for at least one digit
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
        
        return v
    
    @validator('brand_name', 'sender_name')
    def validate_names(cls, v):
        """Validate name fields"""
        if v is not None:
            # Remove extra whitespace
            v = v.strip()
            
            # Check for empty string after stripping
            if not v:
                raise ValueError('Name cannot be empty or only whitespace')
            
            # Check for malicious content
            if re.search(r'[<>"\\]', v):
                raise ValueError('Name contains invalid characters')
        
        return v

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="User password"
    )
    
    @validator('email')
    def validate_email_format(cls, v):
        """Additional email validation"""
        # Convert to lowercase for consistency
        return v.lower()
    
    @validator('password')
    def validate_password_not_empty(cls, v):
        """Ensure password is not empty"""
        if not v or not v.strip():
            raise ValueError('Password cannot be empty')
        return v

# Schema for user response (what we return to the client)
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    plan: PlanType
    subscription_status: SubscriptionStatus
    
    # Optional branding fields
    brand_name: Optional[str] = None
    brand_logo_url: Optional[str] = None
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None
    
    # Stripe integration status
    connected_stripe_account_id: Optional[str] = None
    
    # Settings
    dunning_enabled: bool
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None

# Schema for user update
class UserUpdate(BaseModel):
    brand_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Brand name (1-100 characters)"
    )
    brand_logo_url: Optional[str] = Field(
        None,
        max_length=500,
        description="Brand logo URL (max 500 characters)"
    )
    sender_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Sender name (1-100 characters)"
    )
    sender_email: Optional[EmailStr] = Field(
        None,
        description="Valid email address for sender"
    )
    dunning_enabled: Optional[bool] = Field(
        None,
        description="Enable or disable dunning"
    )
    
    @validator('brand_name', 'sender_name')
    def validate_names(cls, v):
        """Validate name fields"""
        if v is not None:
            # Remove extra whitespace
            v = v.strip()
            
            # Check for empty string after stripping
            if not v:
                raise ValueError('Name cannot be empty or only whitespace')
            
            # Check for malicious content
            if re.search(r'[<>"\\]', v):
                raise ValueError('Name contains invalid characters')
        
        return v
    
    @validator('brand_logo_url')
    def validate_logo_url(cls, v):
        """Validate logo URL"""
        if v is not None:
            v = v.strip()
            if v and not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('Logo URL must start with http:// or https://')
        return v

# Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Token data schema (what's inside the JWT)
class TokenData(BaseModel):
    sub: Optional[str] = None  # subject (user ID)
    email: Optional[str] = None