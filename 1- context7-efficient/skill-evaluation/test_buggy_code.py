"""
Buggy FastAPI Endpoint with Complex Dependency Injection Issues

This code has several subtle bugs that require consulting FastAPI documentation:
1. Incorrect async context manager usage with database sessions
2. Improper dependency scope handling
3. Background task parameter passing issues
4. Missing dependency cleanup
5. Incorrect lifespan event handling

The bugs are NOT syntax errors - the code will run but fail at runtime or produce
incorrect behavior.
"""

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, select
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


# BUG 1: Incorrect async context manager - not using async with
async def get_db():
    session = async_session_maker()
    try:
        yield session
    finally:
        session.close()  # BUG: Should be await session.close()


# BUG 2: Incorrect lifespan - using old @app.on_event instead of lifespan context manager
app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    engine.dispose()  # BUG: Should be await engine.dispose()


# BUG 3: Background task with incorrect parameter passing
def send_email_notification(user_email: str, db_session: AsyncSession):
    """
    BUG: This function is NOT async but receives an AsyncSession
    Background tasks in FastAPI need careful handling of async dependencies
    """
    # This will fail because we can't use async session in sync function
    print(f"Sending email to {user_email}")
    # Can't await in sync function
    # result = db_session.execute(select(User).where(User.email == user_email))


# BUG 4: Incorrect dependency injection scope
class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


# BUG 5: Service dependency without proper async lifecycle
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """
    BUG: This should be an async generator to properly handle cleanup
    and should yield instead of return for proper dependency lifecycle
    """
    return UserService(db)


# Endpoint with multiple bugs
@app.post("/users/")
async def create_user(
    name: str,
    email: str,
    background_tasks: BackgroundTasks,
    user_service: UserService = Depends(get_user_service)
):
    """
    Create a user and send notification email in background.

    BUGS:
    - Background task gets db session which will be closed before task runs
    - No error handling for unique constraint violation
    - Service lifecycle not properly managed
    """
    try:
        user = await user_service.create_user(name, email)

        # BUG 6: Passing db session to background task
        # By the time background task runs, the session will be closed
        background_tasks.add_task(
            send_email_notification,
            user.email,
            user_service.db  # BUG: Session will be closed!
        )

        return {"id": user.id, "name": user.name, "email": user.email}

    except Exception as e:
        # BUG 7: Not properly handling SQLAlchemy IntegrityError
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get user by ID."""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}


# BUG 8: No proper cleanup in dependency
# The database session may not be properly closed in all error scenarios


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
EXPECTED ISSUES WHEN RUNNING THIS CODE:
1. Database sessions not properly closed (resource leak)
2. Background tasks fail because session is closed
3. Deprecation warnings for @app.on_event
4. Potential connection pool exhaustion
5. Improper error handling

CORRECT PATTERNS NEEDED (from FastAPI docs):
1. Use async with for async context managers
2. Use lifespan context manager instead of on_event
3. Background tasks should not depend on request-scoped dependencies
4. Use dependency_overrides or pass serializable data to background tasks
5. Proper async generator pattern for dependencies with cleanup
6. await on async dispose/close methods
"""
