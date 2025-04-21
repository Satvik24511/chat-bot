from fastapi import APIRouter, Depends, HTTPException
from database import users_collection
from utils.roles import role_required

router = APIRouter()

@router.get("/symptoms")
def get_symptoms(user=Depends(role_required(["doctor", "admin", "patient"]))):
    record = users_collection.find_one({"_id": user["user_id"]})
    if not record:
        raise HTTPException(status_code=404, detail="User not found")
    return {"symptoms": record.get("symptoms", [])}