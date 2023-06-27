from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from . import model
from .database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import messages, users, auth, vote 
from .config import settings
# Pass Encryption | We wanna use bcrypt




# This creates tables in Postgres
model.Base.metadata.create_all(bind=engine)
# Call this in our server
app = FastAPI()

# Router

# Decorator passes our function as an object into another defined in function
@app.get("/phantom/who") # Path/route operation. This one is a GET with the default endpoint
# async only needed when it's async
def whoIsPhantom():
    return {"Phantom": "Our Favorite Hellhound - We're SO Proud!"}

@app.get("/")
def welcome():
    return {"Welcome Message": "Python + FastAPI"}

# Gotta put the router here since it reads from the top
app.include_router(messages.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)