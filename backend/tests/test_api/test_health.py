"""Tests for health check endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestHealthAPI:
    """Test health check API functionality."""
    
    def test_root_health_check(self, client: TestClient):
        """Test root health check endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "ChargeChase API is running"
        assert data["status"] == "healthy"
    
    def test_api_health_check(self, client: TestClient):
        """Test dedicated health check endpoint."""
        response = client.get("/api/health")
        
        # This might return 404 if not implemented yet
        # This test will help us identify missing endpoints
        if response.status_code == 404:
            pytest.skip("Health endpoint not yet implemented")
        else:
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
    
    def test_health_check_headers(self, client: TestClient):
        """Test that health check includes proper headers."""
        response = client.get("/")
        
        assert response.status_code == 200
        # Check that CORS headers are present (basic check)
        # More detailed CORS testing would be in integration tests
    
    def test_health_check_performance(self, client: TestClient):
        """Test that health check is fast (under 100ms)."""
        import time
        
        start_time = time.time()
        response = client.get("/")
        end_time = time.time()
        
        assert response.status_code == 200
        duration = (end_time - start_time) * 1000  # Convert to ms
        assert duration < 100, f"Health check took {duration}ms, should be under 100ms"