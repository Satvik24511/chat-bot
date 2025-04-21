import bcrypt
import jwt
import os
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode(), hashed)

def create_jwt(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")