import json

json_file_path = 'patients.json'

def read_json(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def write_json(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def get_all_patients():
    try:
        return read_json(json_file_path)
    except FileNotFoundError:
        return []

def save_new_patient(patient_data):
    patients = get_all_patients()
    patients.append(patient_data)
    write_json(json_file_path, patients)

def find_patient_by_ssn(ssn):
    patients = get_all_patients()
    for patient in patients:
        if patient['ssn'] == ssn:
            return patient
    return None

def delete_patient_by_ssn(ssn):
    patients = get_all_patients()
    patients = [patient for patient in patients if patient['ssn'] != ssn]
    write_json(json_file_path, patients)

def update_patient_by_ssn(ssn, updated_data):
    patients = get_all_patients()
    for i, patient in enumerate(patients):
        if patient['ssn'] == ssn:
            patients[i] = updated_data
            write_json(json_file_path, patients)
            return
    raise HTTPException(status_code=404, detail="Patient not found!")

from fastapi import HTTPException