from typing import List, Optional, Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from schemas.user import  UserCreate, UserOut, Response
from database.database import user_db
from services.user import user_service



user_router = APIRouter()

@user_router.post("", response_model=Response, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    user_out = user_service.create_user(user_in)
    if user_out.username in user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    return Response(message="User created successfully", data=[user_out], has_error=False)



# @user_router.post("", response_model=Response, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserCreate):
#     """Create a new user with standardized response"""
#     try:
#         user_out = user_service.create_user(user)
#         return Response(
#             message="User created successfully",
#             data=[user_out],  # Note the list wrapping
#             has_error=False
#         )
#     except HTTPException as he:
#         return Response(
#             message="Failed to create user",
#             error=str(he.detail),
#             has_error=True
#         )
#     except Exception as e:
#         return Response(
#             message="Internal server error",
#             error=str(e),
#             has_error=True
#         )