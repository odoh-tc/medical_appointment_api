from fastapi import APIRouter, Depends, HTTPException, status
from schemas.doctor import Doctor, DoctorCreate, DoctorBase, doctors
from services.doctor import DoctorService, UserService
from services.patient import get_hash_password
from logger import logger


doctor_router = APIRouter(
    prefix="/doctor",
    tags=["doctor"],
)

@doctor_router.post("/",status_code=status.HTTP_201_CREATED)
async def create_doctor(payload: DoctorCreate):
    try:
        UserService.validate_username(payload)
        
        hashed_password = get_hash_password(payload.password)

        doctor_id = len(doctors) + 1

        new_doctor = Doctor(
            id=doctor_id,
            username=payload.username,
            specialization=payload.specialization,
            phone=payload.phone,
            is_available=payload.is_available,
            password=hashed_password,
        )

        doctors.append(new_doctor)

        return {
            "message": "Doctor created successfully",
            "data": new_doctor
        }
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )



@doctor_router.put("/{doctor_id}/availability", response_model=Doctor)
async def set_doctor_availability(doctor_id: int, is_available: bool):
  
        DoctorService.set_doctor_availability(doctor_id, is_available)
        
        return DoctorService.get_doctor_by_id(doctor_id)
    


@doctor_router.get("/{doctor_id}", status_code=status.HTTP_200_OK)
async def get_doctor(doctor_id: int):

        doctor = DoctorService.get_doctor_by_id(doctor_id)
        
        if doctor:
            return doctor
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found."
            )
        

@doctor_router.put("/{doctor_id}", status_code=status.HTTP_200_OK)
async def update_doctor(doctor_id: int, payload: DoctorCreate):
           
        doctor = DoctorService.get_doctor_by_id(doctor_id)
        
        if doctor:
            doctor.username = payload.username
            doctor.specialization = payload.specialization
            doctor.phone = payload.phone
            doctor.is_available = payload.is_available
            
            return doctor
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found."
            )
   

@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: int):
   
        doctor = DoctorService.get_doctor_by_id(doctor_id)
        
        if doctor:
            doctors.remove(doctor)
            return {"message": "Doctor deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found."
            )
   

@doctor_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_doctors():
    try:
        return doctors
    except Exception as e:
        logger.error(f"Error getting all doctors: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving all doctors information."
        )
