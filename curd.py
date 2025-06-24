from sqlalchemy.future import select
from app.models import User, Message

async def create_user(db, username: str):
    user = User(username=username)
    db.add(user)
    await db.commit()
    return user

async def get_user(db, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def save_message(db, message):
    db.add(message)
    await db.commit()
