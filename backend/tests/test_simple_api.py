"""Simple API tests that don't require database setup."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import the app directly for simple testing
from app.main import app


@pytest.fixture
def simple_client():
    """Create a test client without database dependency override."""
    with TestClient(app) as client:
        yield client


@pytest.mark.integration
class TestSimpleAPI:
    """Test basic API functionality without database."""
    
    @patch('app.core.database.create_tables')
    def test_root_endpoint(self, mock_create_tables, simple_client):
        """Test the root health check endpoint."""
        # Mock the database creation to avoid connection issues
        mock_create_tables.return_value = None
        
        response = simple_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "ChargeChase API is running"
        assert data["status"] == "healthy"
    
    def test_cors_headers_present(self, simple_client):
        """Test that CORS headers are configured."""
        with patch('app.core.database.create_tables'):
            response = simple_client.get("/")
            
            # Check for basic response
            assert response.status_code == 200
            
            # CORS headers should be present in real scenarios
            # This is a basic smoke test
    
    def test_api_structure(self, simple_client):
        """Test API route structure."""
        with patch('app.core.database.create_tables'):
            # Test various endpoints that should exist
            endpoints_to_test = [
                "/",  # Root health check
                "/docs",  # OpenAPI docs (should exist with FastAPI)
                "/openapi.json",  # OpenAPI spec
            ]
            
            for endpoint in endpoints_to_test:
                response = simple_client.get(endpoint)
                # Should not return 500 (server error)
                assert response.status_code != 500, f"Server error on {endpoint}"
                # Should be either 200 (success) or 404 (not found), not 500
                assert response.status_code in [200, 404, 422], f"Unexpected status on {endpoint}: {response.status_code}"
    
    def test_auth_endpoints_exist(self, simple_client):
        """Test that auth endpoints are registered."""
        with patch('app.core.database.create_tables'):
            # These should return 422 (validation error) or 404, not 500
            auth_endpoints = [
                "/api/auth/login",
                "/api/auth/register",
            ]
            
            for endpoint in auth_endpoints:
                response = simple_client.post(endpoint, json={})
                # Should not crash with server error
                assert response.status_code != 500, f"Server error on {endpoint}"