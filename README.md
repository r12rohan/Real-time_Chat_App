# Realtime Chat Messaging App
This application functions similarly to Discord, allowing authenticated users to participate in real-time chat and freely join or leave chat sessions at any time.
* A full-featured Realtime Chat Application built with FastAPI, WebSockets and PostgreSQL.
* Users can sign up, log in and chat in different rooms. 
* Admin functionality (RBAC needs to be implemented):
    * create or Delete rooms
    * Delete users
* Connects user to a room and enables real-time chatting.
* Messages are broadcast to all connected users in that room.

# Features
* User Registration & Login with JWT Authentication.
* Real-time Chat with WebSocket support:
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

4. Once the server is running, open two additional terminal windows and execute the chat_client.py file in each. This will enable real-time communication between the connected clients.