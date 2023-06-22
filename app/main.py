from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import model, schemaz
from .database import engine, get_db
from sqlalchemy.orm import Session


# This creates tables in Postgres
model.Base.metadata.create_all(bind=engine)
# Call this in our server
app = FastAPI()

# This is using psycopg2, using ORM this commit onwards

while True:
    try:
        konect = psycopg2.connect(host='localhost', database='phantom', user='postgres', password='2542', cursor_factory=RealDictCursor)
        cursor = konect.cursor()
        print("Database Connection Successful")
        break
    except Exception as error:
        print("Database Connection Failed")
        print("Error: ", error)
        time.sleep(13)


# Decorator passes our function as an object into another defined in function
@app.get("/phantom/who") # Path/route operation. This one is a GET with the default endpoint
# async only needed when it's async
def whoIsPhantom():
    return {"Phantom": "Our Favorite Hellhound - We're SO Proud!"}

@app.get("/")
def welcome():
    return {"Welcome Message": "Python + FastAPI"}

# Run using uvicorn main:app where app is the instance of main module(file)
@app.post("/saySomething" , status_code = status.HTTP_201_CREATED, response_model = schemaz.MessageResponse)
def yourMessage(msg: schemaz.CreateMessage, db: Session = Depends(get_db)): # Payload has a schema which is the class
    # cursor.execute(""" INSERT INTO public."YourMessages" (name, message, age, employed, salary) VALUES (%s, %s, %s, %s, %s) RETURNING *; """, (payload.name, payload.message, payload.age, payload.employed, payload.salary))
    # new_msg = cursor.fetchone()
    # konect.commit()

    newMsg = model.Message(**msg.dict()) # ** means to unpack the dict same as name=msg.name, message = msg.message, age = msg.age, employed = msg.employed, salary = msg.salary etc
    db.add(newMsg)
    db.commit()
    db.refresh(newMsg)
    return newMsg # dict is hashable, if I returned payload it wouldn't be

@app.get("/yourMessages", response_model = List[schemaz.MessageResponse])
def getMsgs(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public."YourMessages"; """)
    # msgs = cursor.fetchall()
    # return {"data:": msgs}
    messages = db.query(model.Message).all()
    return messages 

@app.get("/yourMessages/{id}", response_model = schemaz.MessageResponse) # Path parameter will always be passed as string
def getMsg(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM public."YourMessages" WHERE id = %s; """, (str(id)),)
    # msg = cursor.fetchone()
    # #     response.status_code = status.HTTP_404_NOT_FOUND 
    # #     return {'message': f'Message with ID {id} not found'}
    # return {"data": msg}
    msg = db.query(model.Message).filter(model.Message.id == id).first()
    if not msg:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    return msg
    #  # Printing this gives you SQL statement


@app.delete("/yourMessages/{id}", status_code=status.HTTP_204_NO_CONTENT)
def getMsg(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM public."YourMessages" WHERE id = %s RETURNING *; """, (str(id)),)
    # msg = cursor.fetchone()
    # konect.commit()
    msg = db.query(model.Message).filter(model.Message.id == id)

    if not msg.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    # #     response.status_code = status.HTTP_404_NOT_FOUND 
    # #     return {'message': f'Message with ID {id} not found'}
    msg.delete(synchronize_session=False)
    db.commit()
    return (f"Deleted Message with ID {id}")

@app.put('/yourMessages/{id}', response_model = schemaz.MessageResponse)
def changeMsg(id: int, msg: schemaz.YourMessage, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE public."YourMessages" SET name = %s, message = %s, age = %s, employed = %s, salary = %s WHERE id = %s RETURNING *;""", (msg.name, msg.message, msg.age, msg.employed, msg.salary, str(id)),)
    # updated = cursor.fetchone()
    # konect.commit()
    update_query = db.query(model.Message).filter(model.Message.id == id)
    if not update_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    
    update_query.update(msg.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemaz.UserResp)
def newUser(user: schemaz.UserCreate, db: Session = Depends(get_db)):
    new_User = model.User(**user.dict())
    db.add(new_User)
    db.commit()
    db.refresh(new_User)

    return new_User