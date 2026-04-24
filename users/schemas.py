from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"

class UpdateProfileSchema(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class TokenSchema(BaseModel):
    access: str
    refresh: str

class ErrorSchema(BaseModel):
    message: str
