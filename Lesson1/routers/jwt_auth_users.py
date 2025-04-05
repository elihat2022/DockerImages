from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


SECRET_KEY = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChOhr3bwU15MQj"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["jwt_auth_users"])
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
        "password": "$2a$12$VUcfq6thEcQSQmtx7QkT/u5KkZvYtEk0mlt/igXVMQpG2ZmKOHif2"
    },
    "Kelly": {
        "username": "kelly2025",
        "name": "Kelly",
        "email": "kelly@gmail.com",
        "disable": False,
        "password": "$2a$12$rS57A1JTtnoyDq67JnxCZuyIyVBmXS1Rgez26FKnUVCQNfKAEOeti"
    },
}


def search_user(username: str):
    
    for key, user_data in user_db.items():
        if user_data["username"] == username:
            return UserDB(**user_data)
    return None  # Devuelve None si no se encuentra el usuario


async def auth_user(token: str=Depends(oauth2)):
    exception =  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        
        
        if username is None:
            raise exception
        user_db = search_user(username)
    # Convertir UserDB a UserBase para eliminar la contraseña
        user = UserBase(
            username=user_db.username,
            name=user_db.name,
            email=user_db.email,
            disable=user_db.disable
        )

    except jwt.JWTError:
        raise exception

    return user




@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user(form.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    

    if not crypt_context.verify(form.password,user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    

    if user.disable:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    expiration= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = {"sub": user.username, "exp": expiration }
    return {"access_token": jwt.encode(access_token, algorithm=ALGORITHM, key=SECRET_KEY), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: UserBase = Depends(auth_user)):
    return user