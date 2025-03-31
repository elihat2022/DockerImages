from fastapi import FastAPI, HTTPException
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

# Path
@app.get("/users")
async def users():
    return user_example
    
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

@app.get("/user/")
async def userQuery(id: int):
    return search_user(id)

@app.post("/user/", response_model=User)
async def create_user(user: User):
    if type(search_user(user.id))==User:
       
        raise HTTPException(status_code=409, detail="User already exists")
    
    else:
        user_example.append(user)
        raise HTTPException(status_code=201, detail="User created")

@app.put("/user/")
async def user_update(user: User):
    for index, user_saved in  enumerate(user_example):
        try: 
            if user_saved.id == user.id:
                user_example[index] = user
                return {"User updated"}
        except:
            return {"error": "User not found"}


@app.delete("/user/")
def delete_user(id: int):
    user = search_user(id)
    for index, user in enumerate(user_example):
        try:
            if user.id == id:
             user_example.pop(index)
             return {f"The user {user.name} was deleted"}
        except:
            return {"error": "user not found"}

def search_user(id: int):
    filtered_user = filter(lambda x: x.id == id, user_example)
    try:
        return list(filtered_user)[0]
    except IndexError:
        raise HTTPException(status_code=404)
    except ValueError:
        return {"error": "Invalid ID format"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)