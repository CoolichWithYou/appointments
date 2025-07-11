from datetime import datetime

from pydantic import BaseModel, field_validator


class AppointmentModel(BaseModel):
    doctor_id: int
    patient_id: int
    start_time: datetime
    end_time: datetime

    @field_validator("start_time", "end_time")
    def remove_timezone(cls, value):
        if isinstance(value, str) and value.endswith("Z"):
            value = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(value) if isinstance(value, str) else value
        return dt.replace(tzinfo=None)


class AppointmentModelOutput(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    start_time: datetime
    end_time: datetime


class PatientModel(BaseModel):
    name: str
    phone: str


class PatientModelOutput(BaseModel):
    id: int
    name: str
    phone: str


class DoctorModel(BaseModel):
    full_name: str


class DoctorModelOutput(BaseModel):
    id: int
    full_name: str


class SpecialityModel(BaseModel):
    title: str


class SpecialityModelOutput(BaseModel):
    id: int
    title: str
