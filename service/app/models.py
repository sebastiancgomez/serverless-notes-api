from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    id: int
    title: str
    owner: str

class NoteCreate(BaseModel):
    title: str

class LoginRequest(BaseModel):
    username: str
    password: str