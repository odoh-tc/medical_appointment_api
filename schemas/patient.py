from pydantic import BaseModel



class PatientDetail(BaseModel):
    username: str
    first_name: str
    last_name: str
    age: int
    sex: str
    weight: float
    height: float
    phone_number: str


class PatientCreate(PatientDetail):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "example",
                "first_name": "Tochukwu",
                "last_name": "Odoh", 
                "age": 20,
                "sex": "male",
                "weight": 65,
                "height": 1.5,
                "phone_number": "+1234567890",
                "password": "password"
            }
        }

class Patient(PatientCreate):
    id: int



patients: list[Patient] = []
