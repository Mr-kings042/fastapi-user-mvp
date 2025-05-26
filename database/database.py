from schemas.user import UserInDB, UserOut, UserCreate
from typing import Dict


user_db: Dict[str, UserInDB] = {}
user_id_counter: int = 0
