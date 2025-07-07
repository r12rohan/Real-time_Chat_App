from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from uuid import UUID


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: UUID):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
