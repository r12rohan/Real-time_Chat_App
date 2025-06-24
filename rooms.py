from typing import Dict

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    def join(self, room: str, username: str, ws: WebSocket):
        self.rooms.setdefault(room, {})[username] = ws

    def leave(self, room: str, username: str):
        if room in self.rooms and username in self.rooms[room]:
            del self.rooms[room][username]

    async def broadcast(self, room: str, message: str):
        for ws in self.rooms.get(room, {}).values():
            await ws.send_text(message)

room_manager = RoomManager()
