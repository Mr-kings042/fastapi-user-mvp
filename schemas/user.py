from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union, Annotated


class UserBase(BaseModel):
    username: Annotated[str ,Field(..., min_length=3, max_length=5000)]
    email: EmailStr
    full_name: Annotated[Optional[str] , Field(None, max_length=10000)]

class UserCreate(UserBase):
    password: Annotated[str,Field(..., min_length=8, max_length=10000)]


class UserOut(UserBase):
    id: int

class UserInDB(UserBase):
    id: int
    hashed_password: str

class LoginUser(BaseModel):
    username: Annotated[str, Field(..., min_length=3, max_length=5000)]
    password: Annotated[str, Field(..., min_length=8, max_length=10000)]
class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    data: Optional[Union[UserOut, List[UserOut]]] = None
    error: Optional[str] = None


def password_to_hash(password: str) -> str:
    return "hashed_" + password
def save_user(user_in: UserCreate):
    hashed_password = password_to_hash(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    user_out = UserOut(**user_in_db.model_dump(exclude={'hashed_password'}))
    
    return Response(
        message="User created successfully",
        data=user_out,  
        has_error=False
    )
