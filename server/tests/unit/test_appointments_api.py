from datetime import datetime

import asyncpg
import pytest

from server.main import add_doctor, add_patient, postapp
from server.schema import AppointmentModel, DoctorModel, PatientModel
from server.settings import Settings

settings = Settings()

connection = None


async def get_connection():
    async with connection.acquire() as conn:
        yield conn


@pytest.mark.asyncio
async def test_create_appointment() -> None:
    connection = await asyncpg.create_pool(dsn=settings.get_connection())

    patient = PatientModel(name="dmitry", phone="+9112345678")
    doctor = DoctorModel(full_name="ivan ivanovich")

    patient = await add_patient(patient, conn=connection)
    doctor = await add_doctor(doctor, conn=connection)
    appointment = AppointmentModel(
        doctor_id=doctor.id,
        patient_id=patient.id,
        start_time=datetime(2025, 1, 1, 10, 0),
        end_time=datetime(2025, 1, 1, 11, 0),
    )
    appointment = await postapp(appointment, conn=connection)

    assert appointment.doctor_id == doctor.id
