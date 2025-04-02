from fastapi import APIRouter
from pydantic import BaseModel



router = APIRouter(tags=["Products"])

# Path
@router.get("/products")
async def products():
    return ["Producto 1","Producto 2" ]