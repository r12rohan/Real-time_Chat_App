# FastAPI-Chat
# Realtime Chat Messaging App
It is similar to Discord, where authenticated users can chat and join or leave at any time.
* A full-featured Realtime Chat Application built with FastAPI, WebSockets and PostgreSQL.
* Users can sign up, log in and chat live in different rooms. 
* Also includes functionality to delete users. 
* Admin functionality (RBAC needs to be implemented):
    * create rooms / Delete rooms
    * Delete users
* Connects the user to a room and enables real-time chatting.
* Messages are broadcast to all connected users in that room.

# Features
* User Registration & Login with JWT Authentication.
* Realtime Chat with WebSocket support:
    * Join or leave chat rooms.
* Delete user functionality.
* Clean architecture (routers, services, utils, schemas).

# Tech Stack
* Backend: FastAPI (Python)
* Database: PostgreSQL + SQLAlchemy (Async)
* Authentication: JWT (JSON Web Token)
* Password Hashing: Passlib
* WebSockets: FastAPI WebSocket

# API Endpoints
* POST /signup - Register a new user.
* POST /login - Login and get JWT token.
* DELETE /delete-user?user_id=<UUID> - Delete user by ID.
* POST /rooms/ – Create a new chat room.
* GET /rooms/ – List all available chat rooms.
* DELETE /rooms/{room_id} – Delete a chat room by its ID.
* websocket /ws/chat/{room_name}/{username}


# How to Run
1. Clone the repository.

2. Install dependencies.
pip install -r requirements.txt

3. Start the server.
uvicorn main:app --reload
Server will be running at:
http://localhost:8000

4. After starting the server, open two additional terminals and run the chat_client.py file. After that, you can start chatting in real time.