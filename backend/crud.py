# This file contains CRUD operations for the database.
from sqlalchemy.orm import Session

from backend.models import Patient, Doctor, Appointment
from datetime import datetime

# Create a new patient
def create_patient(db, patient):
    
    db.add(patient)

    db.commit()

    db.refresh(patient)

    return patient


# Get All Patients
def get_all_patients(db):
    
    return db.query(Patient).all()


# Get Patient by ID
def get_patient_by_id(db, patient_id):
    
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )


# Update Patient
def update_patient(db, patient_id, patient_data):
    
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if patient:

        patient.full_name = patient_data.full_name
        patient.age = patient_data.age
        patient.gender = patient_data.gender
        patient.phone = patient_data.phone
        patient.email = patient_data.email

        db.commit()

        db.refresh(patient)

    return patient


def patient_exists(db, patient_id):
    
    return (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )


# Delete Patient
def delete_patient(db, patient_id):
    
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if patient:

        db.delete(patient)

        db.commit()

        return True

    return False



# Create a new doctor
def create_doctor(db, doctor):
    
    db.add(doctor)

    db.commit()

    db.refresh(doctor)

    return doctor


# Get All Doctors
def get_all_doctors(db):
    
    return db.query(Doctor).all()


# Get Doctors by Department
def get_doctors_by_department(db, department):
    
    return (
        db.query(Doctor)
        .filter(Doctor.department == department)
        .all()
    )
    
 
# Check if a doctor exists by ID
def doctor_exists(db, doctor_id):

    return (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )    

 
 
# check if a doctor has an appointment at a specific date and time
def is_slot_booked(db, doctor_id, appointment_date, appointment_time):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == appointment_time,
            Appointment.status == "Booked"
        )
        .first()
    )

    return appointment is not None 


# Book Appointment 
def create_appointment(db, appointment):
    
    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    return appointment    

# Get All Appointments
def get_all_appointments(db):
    
    return db.query(Appointment).all()


# Get Appointments by Patient ID
def cancel_appointment(db, appointment_id):
    
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if appointment:

        appointment.status = "Cancelled"

        db.commit()

        db.refresh(appointment)

    return appointment


# Reschedule Appointment
def reschedule_appointment(
    db,
    appointment_id,
    appointment_date,
    appointment_time
):

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if appointment:

        appointment.appointment_date = appointment_date
        appointment.appointment_time = appointment_time

        db.commit()

        db.refresh(appointment)

    return appointment



def is_doctor_available(db, doctor_id, appointment_date):

    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == doctor_id)
        .first()
    )

    if doctor is None:
        return False

    weekday = appointment_date.strftime("%A")

    available_days = [
        day.strip()
        for day in doctor.available_days.split(",")
    ]

    return weekday in available_days