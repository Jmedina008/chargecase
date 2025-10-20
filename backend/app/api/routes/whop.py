from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.core.database import get_db
from app.core.whop_auth import get_current_whop_user, get_whop_company_with_auth, verify_whop_webhook
from app.models import WhopCompany, WhopUser, WhopCustomer, RecoveryEvent, RecoveryStatus
from app.services.whop_payments import whop_payment_service
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/whop", tags=["whop"])


# Pydantic schemas for API responses
class CompanySettingsUpdate(BaseModel):
    brand_color: Optional[str] = None
    custom_message: Optional[str] = None
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None
    retry_schedule: Optional[str] = None
    dunning_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None


class StatsResponse(BaseModel):
    total_recovered: float
    failed_payments: int
    recovery_rate: float
    this_month: float
    active_members: int


class RecentActivity(BaseModel):
    event_type: str
    amount: float
    customer_email: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@router.get("/companies/{company_id}/connection")
async def check_stripe_connection(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Check if company has connected their Stripe account"""
    return {
        "isConnected": bool(company.connected_stripe_account_id),
        "connectedAt": company.stripe_connected_at,
        "accountId": company.connected_stripe_account_id
    }


@router.get("/companies/{company_id}/stats", response_model=StatsResponse)
async def get_company_stats(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Get recovery statistics for a company"""
    
    # Calculate date ranges
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Query statistics
    total_recovered = db.query(func.sum(RecoveryEvent.amount)).filter(
        RecoveryEvent.company_id == company.id,
        RecoveryEvent.event_type == "payment_recovered"
    ).scalar() or 0
    
    failed_payments = db.query(func.count(RecoveryEvent.id)).filter(
        RecoveryEvent.company_id == company.id,
        RecoveryEvent.event_type == "payment_failed"
    ).scalar() or 0
    
    this_month = db.query(func.sum(RecoveryEvent.amount)).filter(
        RecoveryEvent.company_id == company.id,
        RecoveryEvent.event_type == "payment_recovered",
        RecoveryEvent.created_at >= month_start
    ).scalar() or 0
    
    active_members = db.query(func.count(WhopCustomer.id.distinct())).filter(
        WhopCustomer.company_id == company.id,
        WhopCustomer.recovery_status.in_([RecoveryStatus.PENDING, RecoveryStatus.IN_PROGRESS])
    ).scalar() or 0
    
    # Calculate recovery rate
    total_failed = db.query(func.sum(RecoveryEvent.amount)).filter(
        RecoveryEvent.company_id == company.id,
        RecoveryEvent.event_type == "payment_failed"
    ).scalar() or 1  # Avoid division by zero
    
    recovery_rate = (total_recovered / total_failed * 100) if total_failed > 0 else 0
    
    return StatsResponse(
        total_recovered=total_recovered / 100,  # Convert cents to dollars
        failed_payments=failed_payments,
        recovery_rate=min(recovery_rate, 100),  # Cap at 100%
        this_month=this_month / 100,
        active_members=active_members
    )


@router.get("/companies/{company_id}/activity")
async def get_recent_activity(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get recent recovery activity for a company"""
    
    events = db.query(RecoveryEvent).join(WhopCustomer).filter(
        RecoveryEvent.company_id == company.id
    ).order_by(desc(RecoveryEvent.created_at)).limit(limit).all()
    
    activity = []
    for event in events:
        activity.append({
            "event_type": event.event_type,
            "amount": event.amount / 100,  # Convert to dollars
            "customer_email": event.customer.email,
            "created_at": event.created_at,
            "metadata": json.loads(event.metadata) if event.metadata else None
        })
    
    return activity


@router.get("/companies/{company_id}/settings")
async def get_company_settings(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Get company settings"""
    return {
        "brand_color": company.brand_color,
        "custom_message": company.custom_message,
        "sender_name": company.sender_name,
        "sender_email": company.sender_email,
        "retry_schedule": company.retry_schedule,
        "dunning_enabled": company.dunning_enabled,
        "email_enabled": company.email_enabled
    }


@router.post("/companies/{company_id}/settings")
async def update_company_settings(
    company_id: str,
    settings: CompanySettingsUpdate,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Update company settings"""
    
    # Update provided fields
    if settings.brand_color is not None:
        company.brand_color = settings.brand_color
    if settings.custom_message is not None:
        company.custom_message = settings.custom_message
    if settings.sender_name is not None:
        company.sender_name = settings.sender_name
    if settings.sender_email is not None:
        company.sender_email = settings.sender_email
    if settings.retry_schedule is not None:
        company.retry_schedule = settings.retry_schedule
    if settings.dunning_enabled is not None:
        company.dunning_enabled = settings.dunning_enabled
    if settings.email_enabled is not None:
        company.email_enabled = settings.email_enabled
    
    db.commit()
    db.refresh(company)
    
    return {"message": "Settings updated successfully"}


@router.post("/companies/{company_id}/stripe/connect")
async def initiate_stripe_connect(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Initiate Stripe Connect flow for a company"""
    
    # TODO: Implement actual Stripe Connect OAuth flow
    # This would redirect to Stripe with the company's info
    
    stripe_connect_url = f"https://connect.stripe.com/oauth/authorize?response_type=code&client_id=ca_your_client_id&scope=read_write&state={company_id}"
    
    return {
        "connect_url": stripe_connect_url,
        "company_id": company_id
    }


@router.get("/companies/{company_id}/billing")
async def get_billing_info(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Get billing information for a company"""
    return {
        "total_recovered": company.total_recovered / 100,  # Convert to dollars
        "total_fees_owed": company.total_fees_owed / 100,
        "total_fees_paid": company.total_fees_paid / 100,
        "fee_percentage": whop_payment_service.fee_percentage * 100,  # As percentage
        "payment_methods": await whop_payment_service.get_payment_methods(company.whop_company_id)
    }


@router.post("/companies/{company_id}/billing/process")
async def process_pending_fees(
    company_id: str,
    company: WhopCompany = Depends(get_whop_company_with_auth),
    db: Session = Depends(get_db)
):
    """Process pending fees for a company"""
    result = await whop_payment_service.process_batch_fees(db, company)
    return result


@router.post("/webhooks/whop")
async def handle_whop_webhook(
    request: Request,
    webhook_verified: bool = Depends(verify_whop_webhook),
    db: Session = Depends(get_db)
):
    """Handle webhooks from Whop (app installations, etc.)"""
    
    body = await request.json()
    event_type = body.get("type")
    
    if event_type == "app.installed":
        # Handle app installation
        company_data = body.get("company", {})
        
        company = db.query(WhopCompany).filter(
            WhopCompany.whop_company_id == company_data.get("id")
        ).first()
        
        if not company:
            company = WhopCompany(
                whop_company_id=company_data.get("id"),
                whop_owner_id=company_data.get("owner_id"),
                name=company_data.get("name"),
                vanity_url=company_data.get("vanity_url"),
                profile_pic_url=company_data.get("profile_pic_url")
            )
            db.add(company)
            db.commit()
    
    elif event_type == "app.uninstalled":
        # Handle app uninstallation
        company_data = body.get("company", {})
        
        company = db.query(WhopCompany).filter(
            WhopCompany.whop_company_id == company_data.get("id")
        ).first()
        
        if company:
            company.is_active = False
            db.commit()
    
    return {"status": "processed"}


@router.post("/webhooks/stripe/{company_id}")
async def handle_stripe_webhook(
    company_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhooks for payment failures/recoveries"""
    
    # Get company
    company = db.query(WhopCompany).filter(
        WhopCompany.whop_company_id == company_id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # TODO: Verify Stripe webhook signature
    
    body = await request.json()
    event_type = body.get("type")
    
    if event_type == "invoice.payment_failed":
        # Handle failed payment
        invoice = body.get("data", {}).get("object", {})
        customer_id = invoice.get("customer")
        amount = invoice.get("amount_due", 0)
        
        # Get or create customer
        customer = db.query(WhopCustomer).filter(
            WhopCustomer.company_id == company.id,
            WhopCustomer.stripe_customer_id == customer_id
        ).first()
        
        if not customer:
            # Fetch customer details from Stripe
            customer = WhopCustomer(
                company_id=company.id,
                stripe_customer_id=customer_id,
                email=invoice.get("customer_email", "unknown@example.com"),
                name=invoice.get("customer_name"),
                recovery_status=RecoveryStatus.PENDING
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
        
        # Create recovery event
        event = RecoveryEvent(
            company_id=company.id,
            customer_id=customer.id,
            event_type="payment_failed",
            stripe_event_id=body.get("id"),
            stripe_invoice_id=invoice.get("id"),
            amount=amount,
            metadata=json.dumps(body)
        )
        db.add(event)
        
        # Update customer
        customer.total_failed_amount += amount
        customer.last_failed_payment_at = datetime.utcnow()
        customer.recovery_status = RecoveryStatus.IN_PROGRESS
        
        db.commit()
        
        # TODO: Trigger dunning sequence
        
    elif event_type == "invoice.payment_succeeded":
        # Handle recovered payment
        invoice = body.get("data", {}).get("object", {})
        customer_id = invoice.get("customer")
        amount = invoice.get("amount_paid", 0)
        
        customer = db.query(WhopCustomer).filter(
            WhopCustomer.company_id == company.id,
            WhopCustomer.stripe_customer_id == customer_id
        ).first()
        
        if customer:
            # Create recovery event
            event = RecoveryEvent(
                company_id=company.id,
                customer_id=customer.id,
                event_type="payment_recovered",
                stripe_event_id=body.get("id"),
                stripe_invoice_id=invoice.get("id"),
                amount=amount,
                metadata=json.dumps(body)
            )
            db.add(event)
            
            # Update customer and company
            customer.total_recovered_amount += amount
            customer.last_recovered_payment_at = datetime.utcnow()
            customer.recovery_status = RecoveryStatus.RECOVERED
            
            # Update company totals and calculate fees
            company.total_recovered += amount
            fee = whop_payment_service.calculate_fee(amount)
            company.total_fees_owed += fee
            
            db.commit()
            
            # Trigger immediate fee collection for larger amounts
            if amount >= 10000:  # $100 or more recovered
                try:
                    await whop_payment_service.create_transaction_fee_charge(
                        company=company,
                        recovered_amount=amount,
                        transaction_metadata={
                            "immediate_charge": True,
                            "stripe_event_id": body.get("id"),
                            "stripe_invoice_id": invoice.get("id")
                        }
                    )
                    # Reset fees owed since we just charged them
                    company.total_fees_paid += fee
                    company.total_fees_owed -= fee
                    db.commit()
                except Exception as e:
                    # Log error but don't fail the webhook
                    print(f"Failed to charge immediate fee: {str(e)}")
    
    # Update last webhook timestamp
    company.last_webhook_at = datetime.utcnow()
    db.commit()
    
    return {"status": "processed"}