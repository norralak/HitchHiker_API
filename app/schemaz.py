import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Creating schema class for our payload
class YourMessage(BaseModel):
    name: str = "Anonymous"
    message: str
    age: int # Optional field specify the type
    employed: Optional[bool] = False
    salary: Optional[int] = 0

class CreateMessage(YourMessage):
    pass

class MessageResponse(YourMessage):
    id: int
    created: datetime.datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResp(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class MyToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str] = None
