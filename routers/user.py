from typing import List, Optional, Annotated
from uuid import UUID
from fastapi import APIRouter, Form, HTTPException, status
from schemas.user import  LoginUser, UserCreate, Response, UserOut
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

@user_router.get("/Users", response_model=Response, status_code=status.HTTP_200_OK)
def get_all_users():
    users = user_service.get_all_users()
    if not users:
        return Response(message="No users found", data=[], has_error=False)
    
    return Response(message="Users retrieved successfully", data=users, has_error=False)

@user_router.get("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return Response(message="User retrieved successfully", data=user, has_error=False)

@user_router.put("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
def update_user(id: int, user_in: UserCreate):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = user_service.update_user(id, user_in)
    return Response(message="User updated successfully", data=updated_user, has_error=False)
@user_router.delete("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
def delete_user(id: int):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_service.delete_user(id)
    return Response(message="User deleted successfully", data=None, has_error=False)