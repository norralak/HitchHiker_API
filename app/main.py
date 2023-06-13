from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel;
from random import randrange;
# Call this in our server
app = FastAPI()

# Creating schema class for our payload
class YourMessage(BaseModel):
    name: str
    message: str
    age: Optional[int] = None # Optional field specify the type

msgs = {}
# Decorator passes our function as an object into another defined in function
@app.get("/phantom/who") # Path/route operation. This one is a GET with the default endpoint
# async only needed when it's async
def whoIsPhantom():
    return {"Phantom": "Our Favorite Hellhound - We're SO Proud!"}

@app.get("/")
def welcome():
    return {"Welcome Message": "Python + FastAPI"}

# Run using uvicorn main:app where app is the instance of main module(file)
@app.post("/saySomething" , status_code = status.HTTP_201_CREATED)
def yourMessage(payload: YourMessage): # Payload has a schema which is the class
    say_something = payload.dict() # Coverting the payload into a dict
    say_something["id"] = randrange(0, 9999999999)
    msgs[say_something["id"]] = say_something
    print(payload) # Send request to see difference. One is BaseModel object and another is a dictionary
    return {"data": say_something} # dict is hashable, if I returned payload it wouldn't be

@app.get("/yourMessages")
def getMsgs():
    print(type(msgs))
    print(msgs.keys())
    return {"data": msgs}

@app.get("/yourMessages/{id}") # Path parameter will always be passed as string
def getMsg(id: int, response: Response):
    if id not in msgs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    #     response.status_code = status.HTTP_404_NOT_FOUND 
    #     return {'message': f'Message with ID {id} not found'}
    return {"data": msgs[id]}

@app.delete("/yourMessages/{id}")
def getMsg(id: int, response: Response):
    if id not in msgs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    #     response.status_code = status.HTTP_404_NOT_FOUND 
    #     return {'message': f'Message with ID {id} not found'}
    return {"Successfully Deleted": msgs.pop(id) }

@app.put('/yourMessages/{id}')
def changeMsg(id: int, msg: YourMessage):
    if id not in msgs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Message with ID {id} not found')
    msgs[id] = msg
    return {"data": msgs[id]}