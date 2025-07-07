from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from jose import JWTError, jwt
from database import get_db
from models import Room, User, Message
from routers import rooms
from sqlalchemy import select
from services.users_service import get_user_by_username, get_user_by_id
from utils.auth import create_access_token, verify_password
from websocket.manager import manager
from schemas.user import UserCreate, Token



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.include_router(rooms.router)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


# ----------------- Auth Routes -----------------

@app.post("/signup", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user_data.username,
        hashed_password=user_data.password,  # Should be hashed
        email=user_data.email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": new_user.id
    }


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, form_data.username)
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id
    }


# ----------------- Delete User -----------------

@app.delete("/delete-user")
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"msg": "User deleted successfully"}


# ----------------- WebSocket Chat -----------------

@app.websocket("/ws/chat/{room_name}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, username: str):
    db_gen = get_db()
    db = await anext(db_gen)

    try:
        user = await get_user_by_username(db, username)
        if not user:
            await websocket.close(code=1008)
            return

        result = await db.execute(select(Room).where(Room.name == room_name))
        room = result.scalar_one_or_none()
        if not room:
            await websocket.close(code=1003)
            return

        await websocket.accept()
        await manager.connect(websocket)

        while True:
            data = await websocket.receive_text()
            msg = Message(content=data, sender_id=user.id, room_id=room.id)
            db.add(msg)
            await db.commit()
            await manager.broadcast(f"{username}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} has disconnected 💬 (connection closed).")
    finally:
        await db_gen.aclose()

