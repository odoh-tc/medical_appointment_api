from pydantic import BaseModel


class DoctorBase(BaseModel):
    username: str
    specialization: str
    phone: str
    is_available: bool = True


    class Config:
        json_schema_extra = {
            "example": {
                "username": "DrSmith",
                "specialization": "Cardiology",
                "phone": "+1234567890",
                "is_available": True,
                "password": "password"
            }
        }


class DoctorCreate(DoctorBase):
    password: str

class Doctor(DoctorBase):
    id: int

doctors: list[Doctor] = []
