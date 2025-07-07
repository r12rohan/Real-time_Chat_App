# fastapi-chat
# Realtime Chat Messaging App
A full-featured Realtime Chat Application built with FastAPI, WebSockets, and PostgreSQL.
Users can sign up, log in, and chat live in different rooms. Also includes functionality to delete users. Only admin can create new rooms existing users can only enter and chat with other users and leave anytime.

#Features
*User Registration & Login with JWT Authentication
*Realtime Chat with WebSocket support
*Join chat rooms
*Delete user functionality
*Clean architecture (routers, services, utils, schemas)

#Tech Stack
*Backend: FastAPI (Python)
*Database: PostgreSQL + SQLAlchemy (Async)
*Authentication: JWT (JSON Web Token)
*Password Hashing: Passlib
*WebSockets: FastAPI WebSocket

#API Endpoints
*Authentication & User Management
*POST /signup - Register a new user
*POST /token - Login and get JWT token
*DELETE /delete-user?user_id=<UUID> - Delete user by ID

#WebSocket Chat
*ws://localhost:8000/ws/chat/{room_name}/{username}
*Connects the user to a room and enables real-time chatting
*Messages are broadcast to all connected users in that room

#How to Run
1. Clone the repository
git clone https://github.com/your-username/fastapi-chat-app.git
cd codegate

2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables
Create a .env file in the root directory:

DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chatapp
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Start the server
uvicorn main:app --reload
Server will be running at:
http://localhost:8000

After starting the server use two other terminals and run the file chat_client.py and after that you can start chatting in realtime 