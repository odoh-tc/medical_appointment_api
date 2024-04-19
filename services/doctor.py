from typing import Optional
from fastapi import HTTPException, status

from schemas.doctor import Doctor, DoctorCreate, doctors

class UserService:
    @staticmethod
    def validate_username(payload: DoctorCreate):
        username: str = payload.username
        for doctor in doctors:
            if doctor.username == username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with exact name already exists"
                )


class DoctorService:
    @staticmethod
    def find_available_doctor() -> Optional[Doctor]:
        for doctor in doctors:
            if doctor.is_available:
                return doctor
        return None
    

    @staticmethod
    def set_doctor_availability(doctor_id: int, is_available: bool) -> None:
            
            doctor = next((doc for doc in doctors if doc.id == doctor_id), None)
            if doctor:              
                doctor.is_available = is_available
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor not found.",
                )
        

    @staticmethod
    def make_doctor_available(doctor_id: int) -> None:
        
            doctor_index = next((index for index, doc in enumerate(doctors) if doc.id == doctor_id), None)
            if doctor_index is not None:    
                doctors[doctor_index].is_available = True
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor not found.",
                )
        

    @staticmethod
    def get_doctor_by_id(doctor_id: int) -> Optional[Doctor]:
        for doctor in doctors:
            if doctor.id == doctor_id:
                return doctor
        return None