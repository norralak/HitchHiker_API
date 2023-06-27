import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Creating schema class for our payload
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class YourMessage(BaseModel):
    name: str = "Anonymous"
    message: str
    age: int # Optional field specify the type
    employed: Optional[bool] = False
    salary: Optional[int] = 0
    user_id: int
    owner: UserResp
    
class CreateMessage(YourMessage):
    pass

class MessageResponse(BaseModel):
    Message: YourMessage
    votes: int
    
    class Config:
        orm_mode = True

class MyToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    message_id: int
    upDown: Optional[int] = 13

