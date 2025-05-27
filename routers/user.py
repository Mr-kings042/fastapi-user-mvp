from typing import List, Optional, Annotated
from uuid import UUID
from fastapi import APIRouter, Form, HTTPException, status
from schemas.user import  LoginUser, UserCreate, Response
from database.database import user_db
from services.user import user_service



user_router = APIRouter()

@user_router.post("", response_model=Response, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    user_out = user_service.create_user(user_in)
    if user_out.username in user_db.values():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    return Response(message="User created successfully", data=user_out, has_error=False)


@user_router.post("/login", response_model=Response,status_code=status.HTTP_200_OK)
def login_user(user_login: LoginUser):
    user_out = user_service.login_user(user_login)
    if not user_out:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return Response(message="Login successful", data=user_out, has_error=False)