from fastapi import Form, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union, Annotated


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=5000)
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str= Field(..., min_length=6, max_length=10000)


class UserOut(UserBase):
    id: int

class UserInDB(UserBase):
    id: int
    hashed_password: str

class LoginUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=5000)
    password: str = Field(..., min_length=8, max_length=10000)
class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    data: Optional[Union[UserOut, List[UserOut]]] = None
    error: Optional[str] = None


def password_to_hash(password: str) -> str:
    return "hashed_" + password

