from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register():
    return {"message": "User registered successfully"}

@router.post("/login")
async def login():
    return {"message": "User logged in successfully"}
