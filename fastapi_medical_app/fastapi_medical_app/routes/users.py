from fastapi import APIRouter, HTTPException
from database import users_collection
from utils.security import hash_password, verify_password, create_jwt

router = APIRouter()

@router.post("/signup")
def signup(username: str, password: str):
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username exists")
    hashed_pw = hash_password(password)
    user = {
        "username": username,
        "password": hashed_pw,
        "role": "patient",
        "demographics": {},
        "symptoms": []
    }
    users_collection.insert_one(user)
    return {"message": "User created"}

@router.post("/login")
def login(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(user["_id"], user["role"])
    return {"token": token}