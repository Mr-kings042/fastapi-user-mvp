from fastapi import FastAPI
from routers.user import user_router


app = FastAPI(title="User Management API",
              description="API for managing users, including registration and login",
              version="1.0.0")
app.include_router(user_router, prefix="/user", tags=["users"])

app.get("/")
def Home():
    return {"Welcome User MVP the FastAPI application!"}

