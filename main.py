from fastapi import FastAPI
from routers.user import user_router


app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["users"])

app.get("/")
def Home():
    return {"Welcome User MVP the FastAPI application!"}

