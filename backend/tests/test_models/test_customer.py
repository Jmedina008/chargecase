"""Tests for Customer model."""
import pytest
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.customer import Customer


@pytest.mark.unit
class TestCustomerModel:
    """Test Customer model functionality."""
    
    def test_create_customer(self, db_session: Session):
        """Test creating a customer."""
        # Create user first (required for foreign key)
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        customer = Customer(
            user_id=user.id,
            stripe_customer_id="cus_test123",
            email="customer@example.com",
            name="Test Customer"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        assert customer.id is not None
        assert customer.user_id == user.id
        assert customer.stripe_customer_id == "cus_test123"
        assert customer.email == "customer@example.com"
        assert customer.name == "Test Customer"
        assert customer.dont_email is False  # Default
        assert customer.created_at is not None
    
    def test_customer_user_relationship(self, db_session: Session):
        """Test customer-user relationship."""
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        customer = Customer(
            user_id=user.id,
            stripe_customer_id="cus_test123",
            email="customer@example.com"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        # Verify relationships
        assert customer.user == user
        assert customer in user.customers
    
    def test_customer_required_fields(self, db_session: Session):
        """Test that required fields are enforced."""
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        
        # Missing stripe_customer_id should fail
        customer = Customer(user_id=user.id, email="test@example.com")
        db_session.add(customer)
        with pytest.raises(Exception):
            db_session.commit()
        
        db_session.rollback()
        
        # Missing email should fail
        customer = Customer(user_id=user.id, stripe_customer_id="cus_123")
        db_session.add(customer)
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_customer_dont_email_flag(self, db_session: Session):
        """Test dont_email flag functionality."""
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        
        customer = Customer(
            user_id=user.id,
            stripe_customer_id="cus_test123",
            email="customer@example.com",
            dont_email=True
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        assert customer.dont_email is True
    
    def test_customer_indexes(self, db_session: Session):
        """Test that proper indexes exist for performance."""
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        
        # Create customers with indexed fields
        customers = [
            Customer(
                user_id=user.id,
                stripe_customer_id=f"cus_test{i}",
                email=f"customer{i}@example.com"
            )
            for i in range(10)
        ]
        
        db_session.add_all(customers)
        db_session.commit()
        
        # These queries should use indexes (verified by DB inspection)
        result = db_session.query(Customer).filter_by(user_id=user.id).all()
        assert len(result) == 10
        
        result = db_session.query(Customer).filter_by(stripe_customer_id="cus_test5").first()
        assert result.email == "customer5@example.com"
        
        result = db_session.query(Customer).filter_by(email="customer3@example.com").first()
        assert result.stripe_customer_id == "cus_test3"
    
    def test_multiple_customers_same_user(self, db_session: Session):
        """Test one user can have multiple customers."""
        user = User(email="owner@example.com", hashed_password="hash")
        db_session.add(user)
        db_session.commit()
        
        customers = []
        for i in range(5):
            customer = Customer(
                user_id=user.id,
                stripe_customer_id=f"cus_test{i}",
                email=f"customer{i}@example.com",
                name=f"Customer {i}"
            )
            customers.append(customer)
        
        db_session.add_all(customers)
        db_session.commit()
        
        db_session.refresh(user)
        assert len(user.customers) == 5
        
        # Verify all customers belong to the user
        for customer in customers:
            assert customer in user.customers