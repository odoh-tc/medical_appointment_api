from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from middleware import appointment_middleware
from logger import logger
from routers.patient import patient_router
from routers.doctor import doctor_router
from routers.appointment import appointment_router

app = FastAPI(title="Medical Appointment API", 
            version="1.0.0",
             description="An API for managing medical appointments.")


app.add_middleware(BaseHTTPMiddleware, dispatch=appointment_middleware)


app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


logger.info("starting app")


@app.get("/", status_code=status.HTTP_200_OK)
async def home_page():
    return {
        "message": "Welcome to home page"
    }