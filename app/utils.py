# Utilities

from passlib.context import CryptContext

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashIt(password: str) -> str:
    return hasher.hash(password)

def checkPass(password:str, hashed: str):
    return hasher.verify(password, hashed)