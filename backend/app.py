from fastapi import FastAPI

from schemas import PatientData
from prediction import predict_department

from database import engine
from models import Base

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Doctor

import crud
import schemas

from datetime import datetime, date, time
from models import Appointment

from models import Patient
from fastapi import HTTPException

from config import HOSPITAL_OPEN_TIME, HOSPITAL_CLOSE_TIME
from logger import logger

import time as time_module
from fastapi import Request

from ai.llm import ask_llm

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Medical Department Prediction API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "AI Medical Assistant API is running!"}


# add patients
@app.post("/patients")
def add_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db)
):

    new_patient = Patient(
        full_name=patient.full_name,
        age=patient.age,
        gender=patient.gender,
        phone=patient.phone,
        email=patient.email
    )

    return crud.create_patient(
        db,
        new_patient
    )
    
    
# get all patients    
@app.get("/patients")
def get_patients(
    db: Session = Depends(get_db)
):

    return crud.get_all_patients(db)    
    
    
# get patient by id
@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = crud.get_patient_by_id(
        db,
        patient_id
    )

    if patient is None:
        return {"message": "Patient not found"}

    return patient    
  
  
# update patient  
@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: int,
    patient: schemas.PatientUpdate,
    db: Session = Depends(get_db)
):

    updated = crud.update_patient(
        db,
        patient_id,
        patient
    )

    if updated is None:
        return {"message": "Patient not found"}

    return updated    



# Delete patients
@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_patient(
        db,
        patient_id
    )

    if deleted:
        return {
            "message": "Patient deleted successfully."
        }

    return {
        "message": "Patient not found."
    }
    

@app.post("/predict")
def predict(patient: PatientData):

    input_data = {
        "age": patient.age,
        "gender": patient.gender,
        "symptoms": patient.symptoms,
        "temperature": patient.temperature,
        "duration_days": patient.duration_days,
        "blood_pressure_systolic": patient.blood_pressure_systolic,
        "blood_pressure_diastolic": patient.blood_pressure_diastolic,
        "heart_rate": patient.heart_rate,
        "oxygen_saturation": patient.oxygen_saturation,
        "pain_level": patient.pain_level,
        "symptom_severity": patient.symptom_severity,
        "chronic_condition": patient.chronic_condition
    }
    
    logger.info("Prediction request received: %s", input_data)
    
    prediction = predict_department(input_data)

    logger.info("Predicted department: %s", prediction)
    
    return {
        "predicted_department": prediction
    }
    
    
    
@app.post("/doctors")
def add_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db)
):

    new_doctor = Doctor(
        doctor_name=doctor.doctor_name,
        department=doctor.department,
        experience=doctor.experience,
        available_days=doctor.available_days
    )

    return crud.create_doctor(db, new_doctor)    


@app.get("/doctors")
def get_doctors(
    db: Session = Depends(get_db)
):

    return crud.get_all_doctors(db)



@app.get("/doctors/{department}")
def doctors_by_department(
    department: str,
    db: Session = Depends(get_db)
):

    return crud.get_doctors_by_department(
        db,
        department
    )
    

@app.post("/appointments")
def book_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):

    # Check if patient exists
    patient = crud.patient_exists(db, appointment.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    # Check if doctor exists
    doctor = crud.doctor_exists(db, appointment.doctor_id)

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )


    today = date.today()

    if appointment.appointment_date < today:
        raise HTTPException(
            status_code=400,
            detail="Appointment date cannot be in the past."
        )
        
    
    current_time = datetime.now().time()

    if (
        appointment.appointment_date == today
        and appointment.appointment_time <= current_time
    ):
        raise HTTPException(
            status_code=400,
            detail="Appointment time has already passed."
        )   
             
    # Hospital Working Hours Validation
    if (
        appointment.appointment_time < HOSPITAL_OPEN_TIME
        or appointment.appointment_time > HOSPITAL_CLOSE_TIME
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Appointments can only be booked between "
                f"{HOSPITAL_OPEN_TIME.strftime('%H:%M')} and "
                f"{HOSPITAL_CLOSE_TIME.strftime('%H:%M')}."
            )
        )      
        
    # doctor availability check       
    if not crud.is_doctor_available(
        db,
        appointment.doctor_id,
        appointment.appointment_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Doctor is not available on the selected day."
        )         
        
        
    # Check if appointment slot is already booked
    if crud.is_slot_booked(
        db,
        appointment.doctor_id,
        appointment.appointment_date,
        appointment.appointment_time
    ):
        raise HTTPException(
            status_code=409,
            detail="Appointment slot already booked."
        )

    # Create appointment
    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        status="Booked"
    )

    return crud.create_appointment(db, new_appointment)

    
    
@app.get("/appointments")
def get_appointments(
    db: Session = Depends(get_db)
):

    return crud.get_all_appointments(db)



@app.delete("/appointments/{appointment_id}")
def cancel(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = crud.cancel_appointment(
        db,
        appointment_id
    )

    if appointment is None:

        return {
            "message": "Appointment not found."
        }

    return {
        "message": "Appointment cancelled successfully.",
        "appointment": appointment
    }    
    


@app.put("/appointments/{appointment_id}")
def reschedule(
    appointment_id: int,
    appointment_date: date,
    appointment_time: time,
    db: Session = Depends(get_db)
):

    appointment = crud.reschedule_appointment(
        db,
        appointment_id,
        appointment_date,
        appointment_time
    )

    if appointment is None:

        return {
            "message": "Appointment not found."
        }

    return {
        "message": "Appointment rescheduled successfully.",
        "appointment": appointment
    }    
    


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time_module.time()

    response = await call_next(request)

    duration = time_module.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status:{response.status_code} "
        f"Time:{duration:.3f}s"
    )

    return response 


@app.get("/test-llm")
def test_llm():
    response = ask_llm([
        {
            "role": "user",
            "content": "Reply with exactly: OpenAI LLM is working!"
        }
    ])

    return {
        "response": response
    }
    
    
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Medical Assistant API"
    }