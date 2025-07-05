import asyncio
import websockets
import requests

API_BASE_URL = "http://127.0.0.1:8000"  # Change if needed

def fetch_rooms():
    try:
        response = requests.get(f"{API_BASE_URL}/rooms")
        response.raise_for_status()
        return response.json()  # expecting list of room names
    except Exception as e:
        print(f"Failed to fetch rooms: {e}")
        return []

async def chat_client(uri, username):
    async with websockets.connect(uri) as websocket:
        print(f"Connected to chat server as {username}")

        async def send_messages():
            while True:
                msg = input()
                if msg.lower() == "/quit":
                    print("Exiting chat...")
                    await websocket.close()
                    break
                await websocket.send(f"{username}: {msg}")

        async def receive_messages():
            try:
                async for message in websocket:
                    print(f"\n{message}")
            except websockets.ConnectionClosed:
                print("Connection closed by server.")

        await asyncio.gather(send_messages(), receive_messages())

def main():
    username = input("Enter your username: ")

    rooms = fetch_rooms()
    if rooms:
        print("Available rooms:")
        for i, room in enumerate(rooms, 1):
            print(f"{i}. {room}")
        print("0. Enter a custom room name")

        choice = input("Select room number or 0: ").strip()
        if choice == "0":
            room = input("Enter custom room name: ").strip()
        else:
            try:
                idx = int(choice) - 1
                room = rooms[idx]
            except:
                print("Invalid choice, defaulting to no room")
                room = ""
    else:
        print("No rooms fetched, enter room name manually or leave blank:")
        room = input("Room name: ").strip()

    if room:
        uri = f"ws://127.0.0.1:8000/ws/{room}"
    else:
        uri = "ws://127.0.0.1:8000/ws"

    asyncio.run(chat_client(uri, username))

if __name__ == "__main__":
    main()
