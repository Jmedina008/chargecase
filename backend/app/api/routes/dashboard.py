from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
async def dashboard_stats():
    """Dashboard stats endpoint - placeholder"""
    return {"message": "Dashboard stats endpoint - coming soon"}