from schemas.user import UserBase


user_db: dict[str, UserBase] = {}
user_id_counter: int = 0
