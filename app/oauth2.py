from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemaz, database, model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET KEY
SECRET_KEY = settings.SECRET_KEY
# Algorithm to use
ALGORITHM = settings.ALORITHM
# Expiration time
TOKEN_EXPIRATION = settings.TOKEN_EXP

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verifyToken(token: str, cred_exceptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("userId")

        if id is None:
            raise cred_exceptions
        
        token_data = schemaz.TokenData(id=id)
    
    except JWTError:
        raise cred_exceptions
    
    return token_data

def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    cred_ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials.', headers={"WWW-Authenticate": "Bearer"})
    token = verifyToken(token, cred_ex)
    
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
     