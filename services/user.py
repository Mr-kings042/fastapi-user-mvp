from uuid import UUID
from fastapi import HTTPException, status
from schemas.user import LoginUser, UserCreate, UserInDB, UserOut, password_to_hash
from database.database import user_db, user_id_counter
from typing import List, Optional, Annotated



class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> UserOut:
        global user_id_counter
        if user.username in [u.username for u in user_db.values()]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        if user.email in [u.email for u in user_db.values()]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        hashed_password = password_to_hash(user.password)
        user_in_db = UserInDB(
            id=user_id_counter,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password)
        user_db[user_id_counter] = user_in_db

        user_out = UserOut(
            id=user_id_counter,
            username=user.username,
            email=user.email,
            full_name=user.full_name
        )
        user_id_counter += 1
        
        return user_out
    
    @staticmethod
    def login_user(user_data: LoginUser) ->  UserOut:
        # Check if the user exists in the database
        user = None
        for u in user_db.values():
            if u.username == user_data.username:
                user = u
                break
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        # Check if the password matches
        if user.hashed_password != password_to_hash(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or Password"
            )
        user_out = UserOut(**user.model_dump(exclude={"hashed_password"}))
        return user_out




user_service = UserService()