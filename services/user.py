from uuid import UUID
from fastapi import HTTPException, status
from schemas.user import LoginUser, UserCreate, UserInDB, UserOut,Response, password_to_hash
from database.database import user_db, user_id_counter
from typing import List, Optional, Annotated



class UserService:
    @staticmethod
    def create_user(user: UserCreate) -> UserOut:
        global user_id_counter
        if any(u.username == user.username for u in user_db.values()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        if any(u.email == user.email for u in user_db.values()):
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

    @staticmethod
    def get_all_users() -> List[UserOut]:
        if not user_db:
            return []
        users = list(user_db.values())
        if not users:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found",
                data=None
            )
        users_out = [UserOut(**user.model_dump()) for user in users]
        return users_out
    @staticmethod
    def get_user_by_id(id: int) -> Optional[UserOut]:
        user = user_db.get(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_out = UserOut(**user.model_dump())
        return user_out 
    
    @staticmethod
    def update_user(id: int, user: UserCreate) -> UserOut:
        existing_user = user_db.get(id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if any (u.username == user.username and u.id != id for u in user_db.values()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        if any (u.email == user.email and u.id != id for u in user_db.values()):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        hashed_password = password_to_hash(user.password)
        updated_user = UserInDB(
            id=id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        user_db[id] = updated_user
        user_out = UserOut(**updated_user.model_dump())
        return user_out
    @staticmethod
    def delete_user(id: int) -> Response:
        user = user_db.pop(id, None)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return Response(message="User deleted successfully", has_error=False)
user_service = UserService()



