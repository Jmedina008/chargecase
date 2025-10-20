import os
import requests
from sqlalchemy.orm import Session
from app.models import WhopCompany
from typing import Dict, Any
from datetime import datetime
import json


class WhopPaymentService:
    """Service for handling Whop's payment system integration"""
    
    def __init__(self):
        self.whop_api_base = "https://api.whop.com/v1"
        self.app_id = os.getenv("WHOP_APP_ID")
        self.api_key = os.getenv("WHOP_API_KEY")
        self.fee_percentage = 0.029  # 2.9% transaction fee
    
    async def create_transaction_fee_charge(
        self, 
        company: WhopCompany, 
        recovered_amount: int,  # in cents
        transaction_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a transaction fee charge through Whop's payment system
        """
        fee_amount = int(recovered_amount * self.fee_percentage)
        
        payload = {
            "company_id": company.whop_company_id,
            "amount": fee_amount,  # in cents
            "currency": "usd",
            "description": f"ChargeChase transaction fee for ${recovered_amount/100:.2f} recovered",
            "metadata": {
                "app_id": self.app_id,
                "recovered_amount": recovered_amount,
                "fee_percentage": self.fee_percentage,
                "transaction_type": "recovery_fee",
                **(transaction_metadata or {})
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Whop-App-ID": self.app_id,
        }
        
        try:
            response = requests.post(
                f"{self.whop_api_base}/charges",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to create Whop charge: {str(e)}")
    
    async def process_batch_fees(self, db: Session, company: WhopCompany) -> Dict[str, Any]:
        """
        Process accumulated fees for a company
        """
        if company.total_fees_owed <= 0:
            return {"message": "No fees owed", "amount": 0}
        
        try:
            # Create charge through Whop
            charge = await self.create_transaction_fee_charge(
                company=company,
                recovered_amount=company.total_recovered,  # Use total recovered as base
                transaction_metadata={
                    "batch_processing": True,
                    "fees_owed": company.total_fees_owed,
                    "processing_date": datetime.utcnow().isoformat()
                }
            )
            
            # Update company record
            company.total_fees_paid += company.total_fees_owed
            company.total_fees_owed = 0
            db.commit()
            
            return {
                "status": "success",
                "charge_id": charge.get("id"),
                "amount_charged": charge.get("amount"),
                "company_id": company.whop_company_id
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "company_id": company.whop_company_id
            }
    
    async def get_payment_methods(self, company_id: str) -> Dict[str, Any]:
        """
        Get available payment methods for a company through Whop
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Whop-App-ID": self.app_id,
        }
        
        try:
            response = requests.get(
                f"{self.whop_api_base}/companies/{company_id}/payment_methods",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to get payment methods: {str(e)}"}
    
    async def create_subscription_charge(
        self,
        company: WhopCompany,
        plan_type: str = "monthly",  # or "per_seat", "one_time"
        amount: int = None  # in cents, if None will use default pricing
    ) -> Dict[str, Any]:
        """
        Create a subscription-based charge (alternative to transaction fees)
        """
        if amount is None:
            # Default pricing based on plan type
            pricing = {
                "monthly": 5000,  # $50/month
                "per_seat": 100,  # $1 per member
                "one_time": 50000  # $500 one-time
            }
            amount = pricing.get(plan_type, 5000)
        
        payload = {
            "company_id": company.whop_company_id,
            "amount": amount,
            "currency": "usd",
            "description": f"ChargeChase {plan_type} subscription",
            "interval": "month" if plan_type == "monthly" else None,
            "metadata": {
                "app_id": self.app_id,
                "plan_type": plan_type,
                "subscription_type": "app_usage"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Whop-App-ID": self.app_id,
        }
        
        try:
            endpoint = "subscriptions" if plan_type == "monthly" else "charges"
            response = requests.post(
                f"{self.whop_api_base}/{endpoint}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to create Whop subscription: {str(e)}")
    
    def calculate_fee(self, recovered_amount: int) -> int:
        """Calculate transaction fee for a recovered amount"""
        return int(recovered_amount * self.fee_percentage)
    
    async def handle_payment_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhooks from Whop about payment status changes
        """
        event_type = webhook_data.get("type")
        
        if event_type == "charge.succeeded":
            # Payment successful
            charge = webhook_data.get("data", {}).get("object", {})
            return {
                "status": "processed",
                "event": "payment_success",
                "charge_id": charge.get("id"),
                "amount": charge.get("amount")
            }
        
        elif event_type == "charge.failed":
            # Payment failed
            charge = webhook_data.get("data", {}).get("object", {})
            return {
                "status": "processed",
                "event": "payment_failed",
                "charge_id": charge.get("id"),
                "error": charge.get("failure_message")
            }
        
        return {"status": "ignored", "event_type": event_type}


# Global service instance
whop_payment_service = WhopPaymentService()