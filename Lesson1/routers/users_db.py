from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(tags=["UsersDB"])



user_example = []

# Path
@router.get("/userdb", response_model=list[User])
async def users():
    return  users_schema(db_client.users.find())


@router.get("/userdb/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/userdb/", response_model=User)
async def userQuery(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/userdb/", response_model=User)
async def create_user(user: User):

        if type(search_user_by_email(user.email)) == User:
            raise HTTPException(status_code=409, detail="User already exists")
    
        user_dic = dict(user)
        del user_dic["id"] # Eliminamos el id para que Mongo lo genere automáticamente
        
        id = db_client.users.insert_one(user_dic).inserted_id
        new_user =user_schema(db_client.users.find_one({"_id": id})) 

        return  User(**new_user)
    

    

@router.put("/userdb/", response_model=User)
async def user_update(user: User):
    if not user.id:
        raise HTTPException(status_code=400, detail="User ID is required for updates")
        
    try:
        user_dic = dict(user)
        del user_dic["id"]  # Remove ID from update data
        
        # Note the corrected collection name from "user" to "users"
        # And adding $set to update fields, not replace document
        result = db_client.users.find_one_and_update(
            {"_id": ObjectId(user.id)},
            {"$set": user_dic},
            return_document=True  # Return updated document
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
            
        return User(**user_schema(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")


@router.delete("/userdb/{id}")
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    return {"User deleted"}

  
def search_user_by_email(email: str):
    try:
        user = db_client.users.find_one({"email": email})

        return User(**user_schema(user))
    except:
        return {"error": "user not found"}


def search_user(value: str, key):
    try:
        user = db_client.users.find_one({value: key})

        return User(**user_schema(user))
    except:
        return {"error": "user not found"}