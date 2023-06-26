from .. import model, schemaz, utils, oauth2
from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

# Run using uvicorn main:app where app is the instance of main module(file)
@router.post("/" , status_code = status.HTTP_201_CREATED, response_model = schemaz.MessageResponse)
def yourMessage(msg: schemaz.CreateMessage, db: Session = Depends(get_db), getCurrentUser: str = Depends(oauth2.getCurrentUser)): # Payload has a schema which is the class
    # cursor.execute(""" INSERT INTO public."YourMessages" (name, message, age, employed, salary) VALUES (%s, %s, %s, %s, %s) RETURNING *; """, (payload.name, payload.message, payload.age, payload.employed, payload.salary))
    # new_msg = cursor.fetchone()
    # konect.commit()
    print(getCurrentUser)
    newMsg = model.Message(**msg.dict()) # ** means to unpack the dict same as name=msg.name, message = msg.message, age = msg.age, employed = msg.employed, salary = msg.salary etc
    db.add(newMsg)
    db.commit()
    db.refresh(newMsg)
    return newMsg # dict is hashable, if I returned payload it wouldn't be

@router.get("/", response_model = List[schemaz.MessageResponse])
def getMsgs(db: Session = Depends(get_db), getCurrentUser: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute(""" SELECT * FROM public."YourMessages"; """)
    # msgs = cursor.fetchall()
    # return {"data:": msgs}
    messages = db.query(model.Message).all()
    return messages 

@router.get("/{id}", response_model = schemaz.MessageResponse) # Path parameter will always be passed as string
def getMsg(id: int, db: Session = Depends(get_db), getCurrentUser: int = Depends(oauth2.getCurrentUser)):
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def getMsg(id: int, db: Session = Depends(get_db), getCurrentUser: int = Depends(oauth2.getCurrentUser)):
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

@router.put('/{id}', response_model = schemaz.MessageResponse)
def changeMsg(id: int, msg: schemaz.YourMessage, db: Session = Depends(get_db), getCurrentUser: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute(""" UPDATE public."YourMessages" SET name = %s, message = %s, age = %s, employed = %s, salary = %s WHERE id = %s RETURNING *;""", (msg.name, msg.message, msg.age, msg.employed, msg.salary, str(id)),)
    # updated = cursor.fetchone()
    # konect.commit()
    update_query = db.query(model.Message).filter(model.Message.id == id)
    if not update_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    
    update_query.update(msg.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()