from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import ValidationError
from patient import Patient, PatientWithOnlyName
from json_helper import get_all_patients, save_new_patient, find_patient_by_ssn, delete_patient_by_ssn, update_patient_by_ssn

app = FastAPI()

@app.get("/")
def hello_world():
    return "Hello world!"

@app.get("/patients", response_model=List[Patient])
def get_patients():
    return get_all_patients()

@app.post("/patients")
def create_patient(patient: Patient):
    if patient.ssn[5:7] != "91":
        raise HTTPException(status_code=400, detail="Department must be Essonne (91)")
    try:
        serialized_patient = patient.model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_new_patient(serialized_patient)
    return "Patient created successfully!"

@app.get("/patients/{ssn}")
def get_patient(ssn: str):
    patient = find_patient_by_ssn(ssn)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    return patient

@app.delete("/patients/{ssn}")
def delete_patient(ssn: str):
    if not find_patient_by_ssn(ssn):
        raise HTTPException(status_code=404, detail="Patient not found!")
    delete_patient_by_ssn(ssn)
    return "Patient deleted successfully!"

@app.put("/patients/{ssn}")
def update_patient(ssn: str, patient: Patient):
    if not find_patient_by_ssn(ssn):
        raise HTTPException(status_code=404, detail="Patient not found!")
    try:
        serialized_patient = patient.model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    update_patient_by_ssn(ssn, serialized_patient)
    return "Patient updated successfully!"

@app.post("/patients/{ssn}")
def add_patient_unique(ssn: str, data: PatientWithOnlyName):
    try:
        patient = Patient(first_name=data.first_name, last_name=data.last_name, ssn=ssn)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="SSN is not valid!")

    if find_patient_by_ssn(ssn):
        raise HTTPException(status_code=400, detail="Patient already exists!")
    
    try:
        serialized_patient = patient.model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    save_new_patient(serialized_patient)
    return "Patient created successfully!"