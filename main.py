from fastapi import FastAPI # import fast api

app = FastAPI() # making its object

@app.get("/") # endpoint or route

def hello(): # function that will return after hitting this endpoint
    return {'message':'Hellow world'}

@app.get("/about") # another endpoint

def about():
    return {'message':'Campux is education platform'}


# https://vefnpvyzpafbxzewdpzd.supabase.co 

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZlZm5wdnl6cGFmYnh6ZXdkcHpkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDQ0NTg2MCwiZXhwIjoyMDg2MDIxODYwfQ.kayDa0GFF1JqCUq4LQBUsTA6u6E6bnGmb2wr7D1MV4w