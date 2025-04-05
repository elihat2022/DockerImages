from fastapi import FastAPI
from routers import products, users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


# Static
app.mount("/static", app=StaticFiles(directory="static"), name="static")

# Home
@app.get("/")
async def home():
    return {"Home"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

