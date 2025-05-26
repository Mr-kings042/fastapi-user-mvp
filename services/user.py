from uuid import UUID
from fastapi import HTTPException
from schemas.user import UserCreate, UserOut
from database.database import user_db, user_id_counter
from typing import List, Optional, Annotated



class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> UserOut:
        global user_id_counter
        if user.username in user_db:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        if user.email in [u.email for u in user_db.values()]:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
        
        user_id_counter += 1
        user_out = UserOut(
            id=user_id_counter,
            username=user.username,
            email=user.email,
            full_name=user.full_name
        )
        
        user_db[user_id_counter] = user_out
        return user_out
    




user_service = UserService()