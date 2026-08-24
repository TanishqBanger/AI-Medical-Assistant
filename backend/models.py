# This file defines your database tables.
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Text,
    ForeignKey
)

from backend.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(20))
    email = Column(String(100))


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(100))
    department = Column(String(100))
    experience = Column(Integer)
    available_days = Column(String(100))


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    appointment_date = Column(Date)

    appointment_time = Column(Time)

    status = Column(String(30))


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))

    user_message = Column(Text)

    assistant_response = Column(Text)