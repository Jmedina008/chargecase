"""Tests for User model."""
import pytest
from sqlalchemy.orm import Session

from app.models.user import User, PlanType, SubscriptionStatus
from app.models.customer import Customer


@pytest.mark.unit
class TestUserModel:
    """Test User model functionality."""
    
    def test_create_user(self, db_session: Session):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_here",
            brand_name="Test Store"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.plan == PlanType.STARTER  # Default
        assert user.subscription_status == SubscriptionStatus.ACTIVE  # Default
        assert user.is_active is True  # Default
        assert user.dunning_enabled is True  # Default
        assert user.created_at is not None
    
    def test_user_email_unique(self, db_session: Session):
        """Test that user emails are unique."""
        user1 = User(email="test@example.com", hashed_password="hash1")
        user2 = User(email="test@example.com", hashed_password="hash2")
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            db_session.commit()
    
    def test_user_plan_types(self, db_session: Session):
        """Test setting different plan types."""
        user = User(email="test@example.com", hashed_password="hash")
        
        # Test all plan types
        for plan in PlanType:
            user.plan = plan
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            assert user.plan == plan
    
    def test_user_subscription_status(self, db_session: Session):
        """Test setting different subscription statuses."""
        user = User(email="test@example.com", hashed_password="hash")
        
        # Test all subscription statuses
        for status in SubscriptionStatus:
            user.subscription_status = status
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            assert user.subscription_status == status
    
    def test_user_customer_relationship(self, db_session: Session):
        """Test user-customer relationship."""
        user = User(email="test@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Add customers
        customer1 = Customer(
            user_id=user.id,
            stripe_customer_id="cus_123",
            email="customer1@example.com"
        )
        customer2 = Customer(
            user_id=user.id,
            stripe_customer_id="cus_456",
            email="customer2@example.com"
        )
        
        db_session.add_all([customer1, customer2])
        db_session.commit()
        
        # Verify relationship
        db_session.refresh(user)
        assert len(user.customers) == 2
        assert customer1 in user.customers
        assert customer2 in user.customers
    
    def test_user_branding_fields(self, db_session: Session):
        """Test user branding configuration."""
        user = User(
            email="test@example.com",
            hashed_password="hash",
            brand_name="My Store",
            brand_logo_url="https://example.com/logo.png",
            sender_name="Store Owner",
            sender_email="owner@mystore.com"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.brand_name == "My Store"
        assert user.brand_logo_url == "https://example.com/logo.png"
        assert user.sender_name == "Store Owner"
        assert user.sender_email == "owner@mystore.com"
    
    def test_user_stripe_fields(self, db_session: Session):
        """Test user Stripe integration fields."""
        user = User(
            email="test@example.com",
            hashed_password="hash",
            stripe_customer_id="cus_billing123",
            stripe_subscription_id="sub_billing456",
            connected_stripe_account_id="acct_connected123",
            connected_stripe_user_id="usr_connected456",
            stripe_access_token="sk_test_access_token",
            stripe_refresh_token="rt_refresh_token"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Verify billing Stripe fields
        assert user.stripe_customer_id == "cus_billing123"
        assert user.stripe_subscription_id == "sub_billing456"
        
        # Verify connected account fields
        assert user.connected_stripe_account_id == "acct_connected123"
        assert user.connected_stripe_user_id == "usr_connected456"
        assert user.stripe_access_token == "sk_test_access_token"
        assert user.stripe_refresh_token == "rt_refresh_token"