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

def search_user(username: str):
    
    for key, user_data in user_db.items():
        if user_data["username"] == username:
            return UserDB(**user_data)
    return None  # Devuelve None si no se encuentra el usuario

async def get_current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if user.password != form.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    if user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me", response_model=UserBase)
async def me(user: UserBase = Depends(get_current_user)):
    return user