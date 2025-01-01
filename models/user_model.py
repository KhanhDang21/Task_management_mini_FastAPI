from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: Optional[str] = 'User'
