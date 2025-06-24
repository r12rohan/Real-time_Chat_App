from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class MessageCreate(BaseModel):
    content: str
    room: str
    username: str
