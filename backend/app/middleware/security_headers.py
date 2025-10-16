from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import structlog

logger = structlog.get_logger()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses"""
    
    def __init__(
        self,
        app,
        hsts_max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        frame_options: str = "DENY",
        content_type_nosniff: bool = True,
        xss_protection: bool = True,
        referrer_policy: str = "strict-origin-when-cross-origin",
        permissions_policy: str = "geolocation=(), microphone=(), camera=()"
    ):
        super().__init__(app)
        self.hsts_max_age = hsts_max_age
        self.include_subdomains = include_subdomains
        self.frame_options = frame_options
        self.content_type_nosniff = content_type_nosniff
        self.xss_protection = xss_protection
        self.referrer_policy = referrer_policy
        self.permissions_policy = permissions_policy
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to the response"""
        
        response = await call_next(request)
        
        # HTTP Strict Transport Security (HSTS)
        if request.url.scheme == "https":
            hsts_value = f"max-age={self.hsts_max_age}"
            if self.include_subdomains:
                hsts_value += "; includeSubDomains"
            response.headers["Strict-Transport-Security"] = hsts_value
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = self.frame_options
        
        # Prevent MIME sniffing
        if self.content_type_nosniff:
            response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS Protection
        if self.xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = self.referrer_policy
        
        # Permissions Policy (formerly Feature Policy)
        response.headers["Permissions-Policy"] = self.permissions_policy
        
        # Content Security Policy (basic)
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # Remove server information
        response.headers.pop("Server", None)
        
        # Add custom security header
        response.headers["X-Security-Headers"] = "enabled"
        
        logger.debug(
            "Security headers applied",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code
        )
        
        return response

class RequestSizeMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size"""
    
    def __init__(self, app, max_size: int = 16 * 1024 * 1024):  # 16MB default
        super().__init__(app)
        self.max_size = max_size
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check request size and reject if too large"""
        
        # Get content length from headers
        content_length = request.headers.get("content-length")
        
        if content_length:
            content_length = int(content_length)
            if content_length > self.max_size:
                logger.warning(
                    "Request too large",
                    content_length=content_length,
                    max_size=self.max_size,
                    client_ip=request.client.host if request.client else "unknown",
                    path=request.url.path
                )
                
                return Response(
                    content='{"detail": "Request entity too large"}',
                    status_code=413,
                    headers={"Content-Type": "application/json"}
                )
        
        response = await call_next(request)
        return response

def create_security_middleware():
    """Factory function to create security middleware with default settings"""
    return SecurityHeadersMiddleware

def create_request_size_middleware(max_size: int = 16 * 1024 * 1024):
    """Factory function to create request size middleware"""
    def middleware_factory(app):
        return RequestSizeMiddleware(app, max_size=max_size)
    return middleware_factory