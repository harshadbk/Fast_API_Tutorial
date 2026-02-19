from fastapi import FastAPI , Path ,HTTPException , Query
from supabase import create_client
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import json
from pydantic import BaseModel , Field , computed_field
from typing import Annotated
load_dotenv()

class Patient(BaseModel):
    patient_id: Annotated[str, Field(..., description="Id of Patient", examples=["P001"])]
    patient_name: Annotated[str, Field(..., description="Name of Patient", examples=["Anjali"])]
    disease: Annotated[str, Field(..., description="Disease of Patient", examples=["Fever"])]
    ward_no: Annotated[int, Field(..., gt=0, lt=10000)]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.ward_no * 2

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 10.5:
            return "UnderWeight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "OverWeight"
        else:
            return "Obese"

app = FastAPI()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def mydata()->int:
    with open("patient.json","r") as f:
        data = json.load(f)

    return data

def savedata(data):
    with open("patient.json","w") as f:
        json.dump(data,f,indent=4)

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
def view_patient(patient_id: str = Path(...,description='Id of patient in DB',example='P001')): # path parameters
    data = mydata()   # list of patients

    for patient in data:
        if patient["patient_id"] == patient_id:
            return patient

    return {"error": "patient_id not found"}

@app.post("/add_patient")
def addpatient(patient_id: str,patient_name:str,disease:str,ward_no:int):

    with open("patient.json","r") as f:
        data = json.load(f)
    
    new_patient = {
        "patient_id" : patient_id,
        "patient_name" : patient_name,
        "disease" : disease,
        "word_no" : ward_no
    }

    data.append(new_patient)

    with open("patient.json","w") as f:
        json.dump(data,f,indent=4)

    return {
        "message": "Patient added successfully",
        "data": new_patient
    }


@app.delete("/delete_patient/{patient_id}")

def delete_p(patient_id: str = Path(...,description='Id of patient in DB to be Deleted',example='P001')):
    
    with open("patient.json", "r") as f:
        data = json.load(f)

    original_length = len(data)

    data = [
        patient for patient in data
        if patient["patient_id"] != patient_id
    ]

    if len(data) == original_length:
        raise HTTPException(status_code=402,detail=('Id not found'))

    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Patient deleted successfully"}

@app.get("/sort_patient")
def sort_patient(sort_by:str = Query(...,description='Sort on the basis of Word No'),
                 order:str=Query('asc',description='Sort in asc in desc order')):
    
    if sort_by != 'ward_no':
        raise HTTPException(status_code=400,detail='Invalid field written')
    
    data = mydata()

    reverse = True if order == 'desc' else False

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = mydata()
    new_id = patient.patient_id.upper()
    # check patient id
    for existing_patient in data:
        if existing_patient["patient_id"].upper() == new_id:
            raise HTTPException(
                status_code=400,
                detail="Patient Already Exists"
            )
    # add new patient
    patient_dict = patient.model_dump()
    patient_dict["patient_id"] = new_id
    patient_dict["bmi"] = patient.bmi
    patient_dict["verdict"] = patient.verdict

    data.append(patient_dict)
    savedata(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to Patient API",
            "success": True
        }
    )
