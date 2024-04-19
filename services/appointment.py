from datetime import datetime
from typing import Optional
from logger import logger
from fastapi import HTTPException, status
from schemas.appointment import  Appointment, appointments
from schemas.patient import Patient
from schemas.doctor import Doctor
from services.doctor import DoctorService

class AppointmentService:
    
    @staticmethod
    def create_appointment(patient: Patient, doctor: Doctor, date: datetime) -> Appointment:
            
            if not doctor.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The doctor is not available for appointments.",
                )

            existing_appointment = AppointmentService.get_existing_appointment(patient.id)
            if existing_appointment:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"You already have an appointment with a doctor. "
                        "If you want to make a new appointment, please cancel the existing one first."
                )
            
            appointment_id = len(appointments) + 1
            new_appointment = Appointment(
                id=appointment_id,
                patient=patient,
                doctor=doctor,
                date=date,
                is_completed=False
            )
            
            DoctorService.set_doctor_availability(doctor.id, False)
            appointments.append(new_appointment)
            return new_appointment
        
    
    @staticmethod
    def get_appointment_by_id(appointment_id: int) -> Optional[Appointment]:
        for appointment in appointments:
            if appointment.id == appointment_id:
                return appointment
        return None
    


    @staticmethod
    def update_appointment(appointment: Appointment) -> Appointment:
        try:
            appointment_index = next((index for index, app in enumerate(appointments) if app.id == appointment.id), None)
            if appointment_index is not None:
                appointments[appointment_index] = appointment
                return appointment
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Appointment not found.",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the appointment.",
            )
        

    @staticmethod
    def get_existing_appointment(patient_id: int) -> Optional[Appointment]:
        for appointment in appointments:
            if appointment.patient.id == patient_id and not appointment.is_completed:
                return appointment
        return None
    

    