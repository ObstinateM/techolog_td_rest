from fastapi import FastAPI, HTTPException
from typing import List
from pymongo import MongoClient
from pydantic import  ValidationError
from patient import Patient, PatientWithOnlyName

app = FastAPI()
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.patient_db
patients_collection = db.patients

@app.get("/")
def hello_world():
    return "Hello world!"


@app.get("/patients", response_model=List[Patient])
def get_patients():
    return list(patients_collection.find({}))


@app.post("/patients")
def create_patient(patient: Patient):
    # Ex2: only accept 91 as department
    if patient.ssn[5:7] != "91":
        raise HTTPException(status_code=400, detail="Department must be Essonne (91)")

    try:
        serializedModel = patient.model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    patients_collection.insert_one(serializedModel)
    return "Patient created successfully!"


@app.get("/patients/{ssn}")
def get_patient(ssn: str, sex: bool = False, year: bool = False, month: bool = False, department: bool = False, country: bool = False, birth_index: bool = False, control_key: bool = False):
    patient = patients_collection.find_one({"ssn": ssn})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found!")
    
    serializedPatient = Patient.model_validate(patient).decrypt()
    res = {}

    if sex:
        res['sex'] = serializedPatient["sex"]
    if year:
        res['year'] = serializedPatient["year"]
    if month:
        res['month'] = serializedPatient["month"]
    if department:
        res['department'] = serializedPatient["department"]
    if country:
        res['country'] = serializedPatient["country"]
    if birth_index:
        res['birth_index'] = serializedPatient["birth_index"]
    if control_key:
        res['control_key'] = serializedPatient["control_key"]
    
    return res

    
@app.delete("/patients/{ssn}")
def delete_patient(ssn: str):
    try:
        Patient(first_name="T", last_name="T", ssn=ssn)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="SSN is not valid!")
    
    patients_collection.delete_one({"ssn": ssn})
    return "Patient deleted successfully!"


@app.put("/patients/{ssn}")
def update_patient(ssn: str, patient: Patient):
    try:
        Patient(first_name="T", last_name="T", ssn=ssn)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="SSN is not valid!")
    
    try:
        serializedModel = patient.model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    patients_collection.update_one({"ssn": ssn}, {"$set": serializedModel})
    return "Patient updated successfully!"


@app.post("/patients/{ssn}")
def add_patient_unique(ssn: str, data: PatientWithOnlyName):
    try:
        patient = Patient(first_name=data.first_name, last_name=data.last_name, ssn=ssn)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="SSN is not valid!")

    # Check for duplication
    if patients_collection.find_one({"ssn": ssn}):
        raise HTTPException(status_code=400, detail="Patient already exists!")
    
    try:
        serializedPatient = patient.model_dump()
    # Should never happens, but just in case
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    patients_collection.insert_one(serializedPatient)
    return "Patient created successfully!"

    