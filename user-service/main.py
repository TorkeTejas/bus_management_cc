from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
import uuid
import hashlib

app = FastAPI(title="User Service")

# In-memory storage
users = {}

class User(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    phone_number: str

class UserLogin(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
async def root():
    return {"message": "Welcome to User Service"}

@app.post("/users/register")
async def register_user(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = str(uuid.uuid4())
    user_dict = user.dict()
    user_dict["user_id"] = user_id
    user_dict["password"] = hash_password(user.password)
    users[user_id] = user_dict
    return {"message": "User registered successfully", "user_id": user_id}

@app.post("/users/login")
async def login_user(credentials: UserLogin):
    for user in users.values():
        if user["username"] == credentials.username and user["password"] == hash_password(credentials.password):
            return {
                "message": "Login successful",
                "user_id": user["user_id"],
                "username": user["username"]
            }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id].copy()
    user.pop("password", None)
    return user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 