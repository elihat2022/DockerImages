from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int = 0

user_example = [User(id=1,name="Elihat", surname="Eli", url="https://eli.com", age=25),
                User(id=2,name="Ali", surname="Ali", url="https://ali.com", age=30),
                User(id=3,name="Sara", surname="Ali", url="https://sara.com", age=22),]

@app.get("/users")
async def users():
    return user_example
    
@app.get("/user/{user_id}")
async def user(user_id: int):
    filtered_user = filter(lambda x: x.id == user_id, user_example)
    try:
        return list(filtered_user)[0]
    except IndexError:
        return {"error": "User not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)