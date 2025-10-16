"""Test configuration and fixtures for ChargeChase backend."""
import os
import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import Settings

# Test database URL - use async SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_chargechase.db"

# Override settings for testing
class TestSettings(Settings):
    DATABASE_URL: str = TEST_DATABASE_URL
    SECRET_KEY: str = "test-secret-key-for-testing-only"
    DEBUG: bool = True
    STRIPE_SECRET_KEY: str = "sk_test_fake_key_for_testing"
    STRIPE_WEBHOOK_SECRET: str = "whsec_test_fake_webhook_secret"
    RESEND_API_KEY: str = "re_test_fake_resend_key"

@pytest.fixture(scope="session")
def test_settings():
    """Test settings fixture."""
    return TestSettings()

# Create test database engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
)
TestingAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session override."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "brand_name": "Test Store",
        "sender_name": "Test Sender",
        "sender_email": "sender@example.com"
    }

@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return {
        "stripe_customer_id": "cus_test123456789",
        "email": "customer@example.com",
        "name": "Test Customer"
    }

# Cleanup test database file after tests
def pytest_sessionfinish(session, exitstatus):
    """Clean up test database file after all tests."""
    if os.path.exists("test_chargechase.db"):
        os.remove("test_chargechase.db")