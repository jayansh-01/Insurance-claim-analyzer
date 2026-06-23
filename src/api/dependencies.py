from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db

async def get_async_db(db: AsyncSession = Depends(get_db)) -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency helper to inject the database session.
    """
    yield db
