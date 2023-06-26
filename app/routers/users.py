from .. import model, schemaz, utils
from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemaz.UserResp)
def newUser(user: schemaz.UserCreate, db: Session = Depends(get_db)):
    # Hash Password
    user.password = utils.hashIt(user.password)
    new_User = model.User(**user.dict())
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"E-Mail {user.email} already exists.")
    db.add(new_User)
    db.commit()
    db.refresh(new_User)

    return new_User

@router.get("/{id}", response_model=schemaz.UserResp)
def getUser(id: int, db: Session = Depends(get_db)):

    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID: {id} not found")

    return user
