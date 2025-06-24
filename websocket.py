from fastapi import WebSocket, APIRouter
from app import database, crud, models
from app.rooms import room_manager

router = APIRouter()

@router.websocket("/ws/{room}/{username}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: str):
    await websocket.accept()
    room_manager.join(room, username, websocket)

    try:
        while True:
            content = await websocket.receive_text()
            await room_manager.broadcast(room, f"{username}: {content}")

            async with database.SessionLocal() as db:
                msg = models.Message(content=content, room=room, username=username)
                await crud.save_message(db, msg)
    except:
        room_manager.leave(room, username)
