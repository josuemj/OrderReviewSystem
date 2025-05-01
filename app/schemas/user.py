from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    passwordHash: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]