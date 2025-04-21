from passlib.context import CryptContext
from pymongo import MongoClient

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_pw(p): return pwd.hash(p)

client = MongoClient("mongodb://localhost:27017")      # or your MONGO_URI
users = client["medical_db"]["users"]

# Remove any old admin_user so you can re‑seed safely
users.delete_many({"username": "admin_user"})

# Insert the first admin
users.insert_one({
    "username": "admin_user",
    "email":    "admin@example.com",
    "password": hash_pw("adminpass"),
    "role":     "admin"
})
users.insert_one({
    "username": "doctor_user",
    "email":    "doctor@example.com",
    "password": hash_pw("doctorpass"),
    "role":     "doctor"
})
# users.insert_one({
#     "username": "admisn_user",
#     "email":    "admin@example.com",
#     "password": hash_pw("adminpass"),
#     "role":     "admin"
# })
print("✅ First admin seeded: admin_user / adminpass")
