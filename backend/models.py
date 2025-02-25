from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class Task(Document):
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"


class User(Document):
    username: str
    email: EmailStr
    is_admin: bool = False

    class Settings:
        name = "users"
