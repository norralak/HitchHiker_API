from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel;

# Call this in our server
app = FastAPI()

# Creating schema class for our payload
class YourMessage(BaseModel):
    name: str
    message: str
    age: Optional[int] = None # Optional field specify the type

# Decorator passes our function as an object into another defined in function
@app.get("/phantom/who") # Path/route operation. This one is a GET with the default endpoint
# async only needed when it's async
def whoIsPhantom():
    return {"Phantom": "Our Favorite Hellhound - We're SO Proud!"}

@app.get("/")
def welcome():
    return {"Welcome Message": "Python + FastAPI"}

# Run using uvicorn main:app where app is the instance of main module(file)
@app.post("/saySomething")
def yourMessage(payload: YourMessage): # Payload has a schema which is the class
    say_something = payload.dict() # Coverting the payload into a dict
    print(say_something)
    print(payload) # Send request to see difference. One is BaseModel object and another is a dictionary
    return {"data": say_something} # dict is hashable, if I returned payload it wouldn't be
    