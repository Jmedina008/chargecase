from fastapi import APIRouter

router = APIRouter()

@router.post("/connect-stripe")
async def connect_stripe():
    """Stripe Connect onboarding endpoint - placeholder"""
    return {"message": "Stripe Connect onboarding endpoint - coming soon"}