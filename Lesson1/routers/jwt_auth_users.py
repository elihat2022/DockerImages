from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class UserBase(BaseModel):
    username: str
    name: str
    email: str
    disable: bool


class UserDB(UserBase):
    password: str

user_db = {
    "Elihat": {
        "username": "eli2025",
        "name": "Eli",
        "email": "eli@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "Kelly": {
        "username": "kelly2025",
        "name": "Kelly",
        "email": "kelly@gmail.com",
        "disable": False,
        "password": "123456"
    },
}

@app.get("/users/")
async def me():
    return {"users": user_db}