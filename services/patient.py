from typing import Optional
from fastapi import HTTPException, status
from schemas.patient import Patient, PatientDetail, patients, PatientCreate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class UserService:

    @staticmethod
    def validate_username(payload: PatientCreate):
        username: str = payload.username
        for patient in patients:
            if patient.username == username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with exact name already exists"
                )

 
def get_hash_password(password):
    return pwd_context.hash(password) 

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password) 

def get_patient_from_id(patient_id: int) -> Optional[PatientDetail]:
   
    found_patient = None
    for patient in patients:
        if patient.id == patient_id:
            found_patient = patient
            break

    if found_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return found_patient