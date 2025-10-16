from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.user import TokenData
import structlog

logger = structlog.get_logger()

# HTTP Bearer token scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify the token
        payload = verify_token(credentials.credentials)
        if payload is None:
            logger.warning("Invalid token provided")
            raise credentials_exception
        
        # Extract user info from token
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            logger.warning("Token missing required claims", payload=payload)
            raise credentials_exception
        
        # Get user from database
        user = await UserService.get_user_by_id(db, int(user_id))
        if user is None:
            logger.warning("User not found for valid token", user_id=user_id)
            raise credentials_exception
        
        # Check if user is active
        if not user.is_active:
            logger.warning("Inactive user attempted access", user_id=user_id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )
        
        logger.debug("User authenticated successfully", user_id=user.id, email=user.email)
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Authentication dependency error", error=str(e))
        raise credentials_exception

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active user (same as get_current_user but explicit)
    """
    return current_user

def get_optional_current_user():
    """
    Dependency to get the current user, but allow None (for optional authentication)
    """
    async def _get_optional_current_user(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(
            HTTPBearer(auto_error=False)
        ),
        db: AsyncSession = Depends(get_db)
    ) -> Optional[User]:
        if credentials is None:
            return None
        
        try:
            # Use the same logic as get_current_user but don't raise exceptions
            payload = verify_token(credentials.credentials)
            if payload is None:
                return None
            
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            
            user = await UserService.get_user_by_id(db, int(user_id))
            if user is None or not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.debug("Optional auth failed", error=str(e))
            return None
    
    return _get_optional_current_user