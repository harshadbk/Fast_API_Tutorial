from fastapi import FastAPI # import fast api

app = FastAPI() # making its object

@app.get("/") # endpoint or route

def hello(): # function that will return after hitting this endpoint
    return {'message':'Hellow world'}

@app.get("/about") # another endpoint

def about():
    return {'message':'Campux is education platform'}