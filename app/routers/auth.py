from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, schemaz, utils, oauth2
router = APIRouter(
    tags=['Auth']
)

@router.post('/login', response_model=schemaz.MyToken)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    emailExists = db.query(model.User).filter(model.User.email == creds.username).first()
    if not emailExists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    if not utils.checkPass(creds.password, emailExists.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials.')
    
    # Create token
    access_token = oauth2.create_token(data = {"userId": emailExists.id})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}