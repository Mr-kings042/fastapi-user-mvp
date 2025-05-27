from schemas.user import UserInDB, UserOut, UserCreate



user_db: dict[str, UserInDB] = {}
user_id_counter: int = 0
