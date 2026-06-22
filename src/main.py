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

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }
