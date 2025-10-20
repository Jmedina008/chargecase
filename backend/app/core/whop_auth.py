from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import WhopCompany, WhopUser
import requests
from typing import Optional
import os

security = HTTPBearer()


class WhopAuthService:
    """Service for handling Whop authentication and authorization"""
    
    def __init__(self):
        self.whop_api_base = "https://api.whop.com/v1"
        self.app_id = os.getenv("WHOP_APP_ID")
        self.api_key = os.getenv("WHOP_API_KEY")
    
    async def verify_whop_token(self, token: str) -> dict:
        """Verify a Whop access token and return user info"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "X-Whop-App-ID": self.app_id,
            }
            
            # Verify token with Whop API
            response = requests.get(f"{self.whop_api_base}/me", headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid Whop token: {str(e)}"
            )
    
    async def get_company_from_whop(self, company_id: str, token: str) -> dict:
        """Get company information from Whop API"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "X-Whop-App-ID": self.app_id,
            }
            
            response = requests.get(f"{self.whop_api_base}/companies/{company_id}", headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.RequestException as e:
            raise HTTPException(
                status_code=404,
                detail=f"Company not found: {str(e)}"
            )


whop_auth_service = WhopAuthService()


async def get_current_whop_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> WhopUser:
    """Get current Whop user from token"""
    
    # Verify token with Whop
    whop_user_data = await whop_auth_service.verify_whop_token(credentials.credentials)
    
    # Get or create user in our database
    user = db.query(WhopUser).filter(WhopUser.whop_user_id == whop_user_data["id"]).first()
    
    if not user:
        user = WhopUser(
            whop_user_id=whop_user_data["id"],
            email=whop_user_data.get("email"),
            username=whop_user_data.get("username"),
            profile_pic_url=whop_user_data.get("profile_pic_url")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update user info
        user.email = whop_user_data.get("email") or user.email
        user.username = whop_user_data.get("username") or user.username
        user.profile_pic_url = whop_user_data.get("profile_pic_url") or user.profile_pic_url
        db.commit()
    
    return user


async def get_whop_company(
    company_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> WhopCompany:
    """Get Whop company and ensure user has access"""
    
    # Get company data from Whop
    company_data = await whop_auth_service.get_company_from_whop(company_id, credentials.credentials)
    
    # Get or create company in our database
    company = db.query(WhopCompany).filter(WhopCompany.whop_company_id == company_id).first()
    
    if not company:
        company = WhopCompany(
            whop_company_id=company_id,
            whop_owner_id=company_data["owner_id"],
            name=company_data["name"],
            vanity_url=company_data.get("vanity_url"),
            profile_pic_url=company_data.get("profile_pic_url")
        )
        db.add(company)
        db.commit()
        db.refresh(company)
    else:
        # Update company info
        company.name = company_data["name"]
        company.vanity_url = company_data.get("vanity_url") or company.vanity_url
        company.profile_pic_url = company_data.get("profile_pic_url") or company.profile_pic_url
        db.commit()
    
    return company


async def get_whop_company_with_auth(
    company_id: str,
    user: WhopUser = Depends(get_current_whop_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> WhopCompany:
    """Get company and verify user has access to it"""
    
    company = await get_whop_company(company_id, credentials, db)
    
    # In a real implementation, you'd verify the user has access to this company
    # through the Whop API or by checking membership
    # For now, we'll assume access is granted
    
    return company


# Alternative auth for webhooks (no user token required)
async def verify_whop_webhook(request: Request) -> bool:
    """Verify that a webhook request came from Whop"""
    
    # Get webhook signature from headers
    signature = request.headers.get("X-Whop-Signature")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing webhook signature")
    
    # Verify signature (implementation depends on Whop's webhook signing)
    # This is a placeholder - implement actual signature verification
    webhook_secret = os.getenv("WHOP_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    # TODO: Implement actual signature verification
    # For now, just check if the secret header matches
    provided_secret = request.headers.get("X-Whop-Secret")
    if provided_secret != webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    return True