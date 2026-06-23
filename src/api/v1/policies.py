from fastapi import APIRouter, status

router = APIRouter(prefix="/policies", tags=["Policies"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_policy():
    return {"message": "Policy created successfully"}

@router.get("/")
async def list_policies():
    return {"message": "Policies retrieved successfully"}
