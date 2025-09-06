from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None



    
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str