from .database import Base
from sqlalchemy import TIMESTAMP, Column, Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

class Message(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    message = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    employed = Column(Boolean, nullable=False, server_default="FALSE")
    salary = Column(Integer, nullable=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "Users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default="NOW()")

class Votes(Base):
    __tablename__ = "Votes"
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    message_id = Column(Integer, ForeignKey("Messages.id", ondelete="CASCADE"), primary_key=True)
