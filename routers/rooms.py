from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Room
from pydantic import BaseModel

from database import async_session


router = APIRouter()


class RoomCreate(BaseModel):
    name: str

class RoomResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/rooms/", response_model=RoomResponse)
async def create_room(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).where(Room.name == room.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Room already exists")
    new_room = Room(name=room.name)
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)
    return new_room

@router.get("/rooms/", response_model=list[RoomResponse])
async def list_rooms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room))
    return result.scalars().all()

@router.delete("/rooms/{room_id}", status_code=204)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    await db.delete(room)
    await db.commit()
