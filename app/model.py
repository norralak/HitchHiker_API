from .database import Base
from sqlalchemy import TIMESTAMP, Column, Boolean, Integer, String, text

class Message(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    message = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    employed = Column(Boolean, nullable=False, server_default="FALSE")
    salary = Column(Integer, nullable=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

class User(Base):
    __tablename__ = "Users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default="NOW()")