from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional
from schemas.doctor import Doctor
from schemas.patient import PatientDetail, Patient


class Appointment(BaseModel):
    id: int
    patient: Patient
    doctor: Doctor
    date: datetime
    is_completed: bool = False 


class AppointmentComplete(BaseModel):
    id: int
    patient: PatientDetail
    doctor: Doctor
    date: datetime
    is_completed: bool = False 


class AppointmentCreate(BaseModel):
    patient_id: int

class CompletedAppointmentResponse(BaseModel):
    id: int
    patient_id: int
    patient_username: str
    patient_name: str
    patient_phone_number: str
    doctor: Dict
    date: datetime
    is_completed: bool
    message: str


appointments: list[Appointment] = []
