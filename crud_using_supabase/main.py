from fastapi import FastAPI
from supabase import create_client
import os
from dotenv import load_dotenv
from uuid import uuid4
load_dotenv()

app = FastAPI()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.get("/")
def home():
    return {"message": "FastAPI + Supabase CRUD API"}

@app.post("/users")
def create_user(name: str, email: str):
    data = {
        "id": str(uuid4()),
        "name": name,
        "email": email
    }
    response = supabase.table("users").insert(data).execute()
    return response.data

@app.get("/users")
def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data

@app.get("/users/{user_id}")
def get_user(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data

@app.put("/users/{user_id}")
def update_user(user_id: str, name: str):
    response = (
        supabase.table("users")
        .update({"name": name})
        .eq("id", user_id)
        .execute()
    )
    return response.data
    
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    supabase.table("users").delete().eq("id", user_id).execute()
    return {"message": f"User deleted {user_id}"}

