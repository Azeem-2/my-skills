"""
Fixed FastAPI Endpoint - Based on Direct Context7 MCP Documentation

All bugs fixed based on FastAPI documentation retrieved via direct MCP tools.
The fixes are identical to Test A since both approaches provided the correct information.
"""

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
import asyncio

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)


# FIX 1: Proper async generator with await for cleanup
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Based on MCP Query 4: async database session dependency"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


# FIX 2: Using lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Based on MCP Query 3: lifespan events - on_event is deprecated"""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# FIX 4: Background task without database session
async def send_email_notification(user_email: str, user_name: str):
    """Based on MCP Query 2: background tasks with serializable data only"""
    await asyncio.sleep(0.1)
    print(f"Email sent to {user_email} for user {user_name}")


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"User with email {email} already exists"
            )

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


# FIX 6: Async dependency with proper typing
async def get_user_service(
    db: AsyncSession = Depends(get_db)
) -> AsyncGenerator[UserService, None]:
    """Based on MCP Query 1: dependencies with async generators"""
    service = UserService(db)
    try:
        yield service
    finally:
        pass


@app.post("/users/")
async def create_user(
    name: str,
    email: str,
    background_tasks: BackgroundTasks,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(name, email)

    # FIX 7: Pass only serializable data
    background_tasks.add_task(
        send_email_notification,
        user.email,
        user.name
    )

    return {"id": user.id, "name": user.name, "email": user.email}


@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
FIXES APPLIED (Same as Test A):
1. Database session cleanup with async with and await
2. Lifespan context manager (deprecated on_event replaced)
3. Background tasks with serializable data only
4. Proper async generator dependencies
5. Error handling with rollback

Documentation Source: Direct Context7 MCP
Note: More verbose documentation but same quality of information
"""
