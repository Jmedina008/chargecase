from fastapi import APIRouter

router = APIRouter()

@router.post("/stripe")
async def stripe_webhook():
    """Stripe webhook endpoint - placeholder"""
    return {"message": "Stripe webhook endpoint - coming soon"}