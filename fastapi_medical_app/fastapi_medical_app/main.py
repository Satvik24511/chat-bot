from fastapi import FastAPI
from routes import users, records

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(records.router, prefix="/records", tags=["Records"])