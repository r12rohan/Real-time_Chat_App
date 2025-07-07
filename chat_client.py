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
            print("Failed to fetch rooms.")
            return []
    except Exception as e:
        print(f"Error fetching rooms: {e}")
        return []

import websockets

async def chat(username: str, room: str):
    uri = f"ws://localhost:8000/ws/chat/{room}/{username}"
    print(f"\n Connecting to room: '{room}' as user: '{username}'...")

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected. Type your messages below. Type /quit to exit.\n")

            async def send_messages():
                loop = asyncio.get_event_loop()
                while True:
                    msg = await loop.run_in_executor(None, input, "> ")
                    if msg.lower() == "/quit":
                        await websocket.close()
                        print("Disconnected from chat.")
                        break
                    await websocket.send(msg)

            async def receive_messages():
                try:
                    async for message in websocket:
                        print(f"\n< {message}")
                except websockets.exceptions.ConnectionClosed as e:
                    if e.code == 4001:
                        print("\n Error: User does not exist in database.")
                    else:
                        print("\n Connection closed by server.")
                    return

            await asyncio.gather(send_messages(), receive_messages())

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")



if __name__ == "__main__":
    print("Fetching available rooms...\n")
    rooms = get_rooms()

    if not rooms:
        print("No rooms found on the server.")
        exit(1)

    print("Available rooms:")
    for idx, room in enumerate(rooms, start=1):
        print(f"{idx}. {room}")

    while True:
        try:
            choice = int(input("\nEnter room number to join: "))
            if 1 <= choice <= len(rooms):
                selected_room = rooms[choice - 1]["name"]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    username = input("Enter your username: ")

    try:
        asyncio.run(chat(username, selected_room))
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nConnection closed.")
