import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config.settings import settings
from src.database.base import Base
from src.database.session import engine

# Import models so they are registered on Base.metadata before table creation
from src.models.user import User
from src.models.policy import Policy
from src.models.claim import Claim

# Import routers
from src.api.v1.auth import router as auth_router
from src.api.v1.policies import router as policy_router
from src.api.v1.claims import router as claim_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info("Initializing database tables on startup...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")
    yield
    # Shutdown sequence
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Include routers under global prefix /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(policy_router, prefix="/api/v1")
app.include_router(claim_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }
