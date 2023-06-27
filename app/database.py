from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# Pretty much the same for all projects

# Dependency for SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This is using psycopg2, using ORM this commit onwards
# We can just comment this out

# while True:
#     try:
#         konect = psycopg2.connect(host='localhost', database='phantom', user='postgres', password='2542', cursor_factory=RealDictCursor)
#         cursor = konect.cursor()
#         print("Database Connection Successful")
#         break
#     except Exception as error:
#         print("Database Connection Failed")
#         print("Error: ", error)
#         time.sleep(13)
