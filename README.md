# FastAPI-Chat
# Realtime Chat Messaging App
It is similar to discord where aunthenticated users can chat and get in and out anytime. It does not have Role-Base Access control (RBAC) only superAdmins can create rooms. 
* A full-featured Realtime Chat Application built with FastAPI, WebSockets, and PostgreSQL.
* Users can sign up, log in, and chat live in different rooms. 
* Also includes functionality to delete users. 
* Only admin can create new rooms existing users can only enter and chat with other users and leave anytime.
* Connects the user to a room and enables real-time chatting
* Messages are broadcast to all connected users in that room

# Features
* User Registration & Login with JWT Authentication
* Realtime Chat with WebSocket support
* Join chat rooms
* Delete user functionality
* Clean architecture (routers, services, utils, schemas)

# Tech Stack
* Backend: FastAPI (Python)
* Database: PostgreSQL + SQLAlchemy (Async)
* Authentication: JWT (JSON Web Token)
* Password Hashing: Passlib
* WebSockets: FastAPI WebSocket

# API Endpoints
* Authentication & User Management
* POST /signup - Register a new user
* POST /login - Login and get JWT token
* DELETE /delete-user?user_id=<UUID> - Delete user by ID
* ws://localhost:8000/ws/chat/{room_name}/{username}

# How to Run
1. Clone the repository

2. Install dependencies
pip install -r requirements.txt

3. Start the server
uvicorn main:app --reload
Server will be running at:
http://localhost:8000

4. After starting the server use two other terminals and run the file chat_client.py and after that you can start chatting in realtime 