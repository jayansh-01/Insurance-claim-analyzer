from fastapi import APIRouter, status

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze_claim():
    return {
        "status": "received",
        "message": "Claim received successfully. AI Ingestion pipeline analysis has been triggered."
    }
