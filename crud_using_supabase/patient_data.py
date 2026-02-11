from fastapi import FastAPI
from supabase import create_client
import os
from dotenv import load_dotenv
from uuid import uuid4
import json
load_dotenv()

app = FastAPI()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def mydata():
    with open("patient.json","r") as f:
        data = json.load(f)

    return data

@app.get("/")

def home():
    return {"message": "FastAPI + Supabase CRUD API"}

@app.get("/about")

def about():
    return {"message": "Patinet management system"}

@app.get("/view")
def view():
    data = mydata()
    return data

@app.get("/view_patient/{patient_id}")
def view_patient(patient_id: str):
    data = mydata()   # list of patients

    for patient in data:
        if patient["patient_id"].lower() == patient_id:
            return patient

    return {"error": "patient_id not found"}
