from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
import structlog

logger = structlog.get_logger()

class UserService:
    """Service class for user operations"""
    
    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
        """Create a new user"""
        try:
            # Hash the password
            hashed_password = get_password_hash(user_create.password)
            
            # Create user object
            user = User(
                email=user_create.email,
                hashed_password=hashed_password,
                brand_name=user_create.brand_name,
                sender_name=user_create.sender_name,
                sender_email=user_create.sender_email
            )
            
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            logger.info("User created successfully", user_id=user.id, email=user.email)
            return user
            
        except IntegrityError:
            await db.rollback()
            logger.warning("User creation failed - email already exists", email=user_create.email)
            raise ValueError("Email already registered")
        except Exception as e:
            await db.rollback()
            logger.error("User creation failed", error=str(e))
            raise
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            result = await db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error("Failed to get user by email", email=email, error=str(e))
            raise
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error("Failed to get user by ID", user_id=user_id, error=str(e))
            raise
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        try:
            user = await UserService.get_user_by_email(db, email)
            if not user:
                logger.info("Authentication failed - user not found", email=email)
                return None
            
            if not user.is_active:
                logger.info("Authentication failed - user inactive", email=email)
                return None
            
            if not verify_password(password, user.hashed_password):
                logger.info("Authentication failed - invalid password", email=email)
                return None
            
            logger.info("User authenticated successfully", user_id=user.id, email=email)
            return user
            
        except Exception as e:
            logger.error("Authentication error", email=email, error=str(e))
            raise
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        try:
            user = await UserService.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # Update only provided fields
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            await db.commit()
            await db.refresh(user)
            
            logger.info("User updated successfully", user_id=user.id)
            return user
            
        except Exception as e:
            await db.rollback()
            logger.error("User update failed", user_id=user_id, error=str(e))
            raise