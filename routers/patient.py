from fastapi import APIRouter, Depends, HTTPException, status
from schemas.patient import Patient, PatientCreate, patients
from services.patient import UserService, verify_password, get_hash_password
from logger import logger


patient_router = APIRouter(
    prefix="/patient",
    tags=["patient"],
)


@patient_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_patient(payload: PatientCreate ):
    try:
        
        UserService.validate_username(payload)

        
        patient_id = len(patients) + 1
        
    
        hashed_password = get_hash_password(payload.password)

        
        new_patient_data = payload.dict()
        new_patient_data.update({
            "id": patient_id,
            "password": hashed_password
        })

        new_patient = Patient(**new_patient_data)

        patients.append(new_patient)

        return {
            "message": "Patient created successfully",
            "data": new_patient
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@patient_router.get("/{patient_id}", status_code=status.HTTP_200_OK)
async def get_patient(patient_id: int):
    try:
        patient = next((p for p in patients if p.id == patient_id), None)
        if patient:
            return patient
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@patient_router.put("/{patient_id}", status_code=status.HTTP_200_OK)
async def update_patient(patient_id: int, payload: PatientCreate):
    try:
        
        curr_patient = next((patient for patient in patients if patient.id == patient_id), None)

        if not curr_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )

        
        curr_patient.username = payload.username
        curr_patient.first_name = payload.first_name
        curr_patient.last_name = payload.last_name
        curr_patient.age = payload.age
        curr_patient.sex = payload.sex
        curr_patient.weight = payload.weight
        curr_patient.height = payload.height
        curr_patient.phone_number = payload.phone_number

        return curr_patient

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    


@patient_router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int):
    try:
        patient_index = next((index for index, patient in enumerate(patients) if patient.id == patient_id), None)

        if patient_index is not None:
            
            del patients[patient_index]
            return None
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@patient_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_patients():
    try:
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

