from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request, Response
from typing import Dict, Any
import structlog

logger = structlog.get_logger()

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000/day", "100/hour"]
)

# Custom rate limit exceeded handler
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom handler for rate limit exceeded"""
    client_ip = get_remote_address(request)
    
    logger.warning(
        "Rate limit exceeded",
        client_ip=client_ip,
        path=request.url.path,
        limit=str(exc.detail)
    )
    
    response = Response(
        content=f'{{"detail": "Rate limit exceeded: {exc.detail}", "retry_after": {exc.retry_after}}}',
        status_code=429,
        headers={
            "Retry-After": str(exc.retry_after),
            "X-RateLimit-Limit": str(exc.detail),
            "Content-Type": "application/json"
        }
    )
    return response

# Rate limiting decorators for different endpoint types
class RateLimits:
    """Predefined rate limits for different endpoint categories"""
    
    # Authentication endpoints (more restrictive)
    AUTH_STRICT = ["5/minute", "20/hour", "100/day"]
    
    # General API endpoints
    API_GENERAL = ["30/minute", "300/hour", "1000/day"] 
    
    # Read-only endpoints (less restrictive)
    READ_ONLY = ["100/minute", "1000/hour", "5000/day"]
    
    # Admin/sensitive operations (very restrictive)
    ADMIN = ["2/minute", "10/hour", "50/day"]
    
    # Webhook endpoints
    WEBHOOK = ["60/minute", "1000/hour"]

def get_limiter():
    """Get the limiter instance"""
    return limiter

def apply_rate_limits():
    """Apply rate limiting middleware to the app"""
    return SlowAPIMiddleware