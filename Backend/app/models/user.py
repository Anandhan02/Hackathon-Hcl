from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List

class UserIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserDB(BaseModel):
    id: str | None = None
    name: str
    email: EmailStr
    password_hash: str
    roles: List[str] = ["CUSTOMER"]
    created_at: datetime

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    roles: List[str]

class AuthPayload(BaseModel):
    accessToken: str
    user: UserOut
