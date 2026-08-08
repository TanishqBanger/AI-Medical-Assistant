# Request/response models
from pydantic import BaseModel
from datetime import date, time
from pydantic import BaseModel, EmailStr


class PatientData(BaseModel):  # <--------- ML model input
    age: int
    gender: str
    symptoms: str
    temperature: float
    duration_days: int
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    heart_rate: int
    oxygen_saturation: int
    pain_level: int
    symptom_severity: str
    chronic_condition: str
    

class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    phone: str
    email: EmailStr


class PatientUpdate(BaseModel):
    full_name: str
    age: int
    gender: str
    phone: str
    email: EmailStr


class PatientResponse(BaseModel):
    id: int
    full_name: str
    age: int
    gender: str
    phone: str
    email: EmailStr

    class Config:
        from_attributes = True  
    
    
class DoctorCreate(BaseModel):
    doctor_name: str
    department: str
    experience: int
    available_days: str


class DoctorResponse(BaseModel):
    id: int
    doctor_name: str
    department: str
    experience: int
    available_days: str

    class Config:
        from_attributes = True    
        

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str

    class Config:
        from_attributes = True        