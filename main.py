from fastapi import FastAPI;

# Call this in our server
app = FastAPI()

# Decorator passes our function as an object into another defined in function

@app.get("/phantom/who") # Path/route operation. This one is a GET with the default endpoint
# async only needed when it's async
def whoIsPhantom():
    return {"Phantom": "Our Favorite Hellhound - We're SO Proud!"}

@app.get("/")
def welcome():
    return {"Welcome Message": "Python + FastAPI"}

# Run using uvicorn main:app where app is the instance of main module(file)
