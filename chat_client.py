import asyncio
import websockets
import requests

API_URL = "http://localhost:8000"

def get_rooms():
    try:
        response = requests.get(f"{API_URL}/rooms")
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Failed to fetch rooms.")
            return []
    except Exception as e:
        print(f"⚠️ Error fetching rooms: {e}")
        return []

async def chat(username: str, room: str):
    uri = f"ws://localhost:8000/ws/chat/{room}/{username}"

    print(f"\n🔌 Connecting to room: '{room}' as user: '{username}'...")
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected. Type your messages below. Ctrl+C to exit.\n")
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
                await websocket.send(msg)
                response = await websocket.recv()
                print(f"< {response}")
    except websockets.exceptions.ConnectionClosed:
        print("❌ Connection closed by server.")
    except KeyboardInterrupt:
        print("\n👋 Exiting chat.")

if __name__ == "__main__":
    print("📡 Fetching available rooms...\n")
    rooms = get_rooms()

    if not rooms:
        print("⚠️ No rooms found on the server.")
        exit(1)

    print("Available rooms:")
    for idx, room in enumerate(rooms, start=1):
        print(f"{idx}. {room}")

    while True:
        try:
            choice = int(input("\nEnter room number to join: "))
            if 1 <= choice <= len(rooms):
                selected_room = rooms[choice - 1]
                break
            else:
                print("❌ Invalid choice. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

    username = input("Enter your username: ")
    asyncio.run(chat(username, selected_room))
