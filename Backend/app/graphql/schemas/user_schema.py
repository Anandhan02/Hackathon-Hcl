# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    roles: List[str]

class AuthPayload(BaseModel):
    accessToken: str
    user: UserOut
