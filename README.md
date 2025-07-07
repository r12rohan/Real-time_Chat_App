# fastapi-chat
Realtime Chat Messaging App
A full-featured Realtime Chat Application built with FastAPI, WebSockets, and PostgreSQL. Users can sign up, log in, and chat live in different rooms. Also includes functionality to delete users.

Features
User Registration & Login with JWT Authentication
Realtime Chat with WebSocket support
Join chat rooms
Delete user functionality
Clean architecture (routers, services, utils, schemas)

 Tech Stack
Backend: FastAPI (Python)
Database: PostgreSQL + SQLAlchemy (Async)
Authentication: JWT (JSON Web Token)
Password Hashing: Passlib
WebSockets: FastAPI WebSocket

API Endpoints
Authentication & User Management
POST /signup - Register a new user
POST /token - Login and get JWT token
DELETE /delete-user?user_id=<UUID> - Delete user by ID

WebSocket Chat
ws://localhost:8000/ws/chat/{room_name}/{username}
Connects the user to a room and enables real-time chatting
Messages are broadcast to all connected users in that room
