from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from schemas.patient import Patient
from services.doctor import DoctorService
from services.appointment import AppointmentService
from schemas.appointment import appointments, CompletedAppointmentResponse
from services.patient import get_patient_from_id
from logger import logger

appointment_router = APIRouter(
    prefix="/appointments", 
    tags=["appointments"]
    )

@appointment_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_appointment(patient: Patient = Depends(get_patient_from_id)):
    
        available_doctor = DoctorService.find_available_doctor()
 
        if available_doctor:
            
            appointment = AppointmentService.create_appointment(
                patient=patient,
                doctor=available_doctor,
                date=datetime.now(),
            )
            message = {
                "message": "Appointment successfully created",
                "appointment_details": {
                    "id": appointment.id,
                    "patient": {
                        "username": appointment.patient.username,
                        "first_name": appointment.patient.first_name,
                        "last_name": appointment.patient.last_name,
                        "age": appointment.patient.age,
                        "sex": appointment.patient.sex,
                        "weight": appointment.patient.weight,
                        "height": appointment.patient.height,
                        "phone_number": appointment.patient.phone_number,
                        "id": appointment.patient.id
                    },
                    "doctor": {
                        "username": appointment.doctor.username,
                        "specialization": appointment.doctor.specialization,
                        "phone": appointment.doctor.phone,
                        "is_available": appointment.doctor.is_available
                    },
                    "date": appointment.date,
                    "is_completed": appointment.is_completed 
                 }}
            return  message
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No doctors are available at the moment.",
            )



@appointment_router.post("/{appointment_id}/complete", response_model=CompletedAppointmentResponse,
                          status_code=status.HTTP_201_CREATED)
async def complete_appointment(appointment_id: int):
        
        appointment = AppointmentService.get_appointment_by_id(appointment_id)
        
        if appointment:
            if appointment.is_completed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The appointment with ID {appointment_id} has already been completed."
                )
            
            appointment.is_completed = True
            AppointmentService.update_appointment(appointment)
            DoctorService.make_doctor_available(appointment.doctor.id)

            response_data = {
                "id": appointment.id,
                "patient_id": appointment.patient.id,
                "patient_username": appointment.patient.username,
                "patient_name": f"{appointment.patient.first_name} {appointment.patient.last_name}",
                "patient_phone_number": appointment.patient.phone_number,
                "doctor": {
                    "username": appointment.doctor.username,
                    "specialization": appointment.doctor.specialization,
                    "phone": appointment.doctor.phone,
                    "is_available": appointment.doctor.is_available
                },
                "date": appointment.date,
                "is_completed": appointment.is_completed,
                "message": "Appointment completed successfully. Doctor is now available for another appointment."
            }
            
            return response_data
            
            
        else:
           
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Appointment with ID {appointment_id} not found."
            )


@appointment_router.delete("/{appointment_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(appointment_id: int):

        appointment = AppointmentService.get_appointment_by_id(appointment_id)
        
        if appointment:
            if appointment.is_completed:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This appointment has already been completed and cannot be canceled."
                )
            
            DoctorService.make_doctor_available(appointment.doctor.id)
            
            appointments.remove(appointment)
            
            return {"message": "Appointment canceled successfully"}
            
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found."
            )
