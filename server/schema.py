from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class DoctorSpecialityBase(SQLModel):
    doctor_id: int = Field(foreign_key="doctor.id", nullable=False)
    patient_id: int = Field(foreign_key="patient.id", nullable=False)
    start_time: datetime
    end_time: datetime


class DoctorSpecialityCreate(DoctorSpecialityBase):
    pass


class DoctorSpeciality(DoctorSpecialityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id", nullable=False)
    speciality_id: int = Field(foreign_key="speciality.id", nullable=False)

    doctor: Optional["Doctor"] = Relationship(
        back_populates="doctor_specialities",
    )
    speciality: Optional["Speciality"] = Relationship(
        back_populates="doctor_specialities"
    )


class AppointmentBase(SQLModel):
    doctor_id: int = Field(foreign_key="doctor.id", nullable=False)
    patient_id: int = Field(foreign_key="patient.id", nullable=False)
    start_time: datetime
    end_time: datetime


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    doctor: Optional["Doctor"] = Relationship(back_populates="appointments")
    patient: Optional["Patient"] = Relationship(back_populates="appointments")


class DoctorBase(SQLModel):
    full_name: str = Field(max_length=100)


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    doctor_specialities: List[DoctorSpeciality] = Relationship(
        back_populates="doctor",
    )
    appointments: List[Appointment] = Relationship(back_populates="doctor")

    specialities: List["Speciality"] = Relationship(
        back_populates="doctors", link_model=DoctorSpeciality
    )
    patients: List["Patient"] = Relationship(
        back_populates="doctors", link_model=Appointment
    )


class PatientBase(SQLModel):
    name: str = Field(max_length=40)
    phone: Optional[str] = Field(default=None, unique=True, max_length=11)


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    appointments: List[Appointment] = Relationship(back_populates="patient")

    doctors: List["Doctor"] = Relationship(
        back_populates="patients", link_model=Appointment
    )


class SpecialityBase(SQLModel):
    title: str = Field(max_length=100)


class SpecialityCreate(SpecialityBase):
    pass


class Speciality(SpecialityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    doctor_specialities: List[DoctorSpeciality] = Relationship(
        back_populates="speciality"
    )

    doctors: List[Doctor] = Relationship(
        back_populates="specialities", link_model=DoctorSpeciality
    )
