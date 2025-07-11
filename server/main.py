from contextlib import asynccontextmanager
from typing import List

import asyncpg
from fastapi import Depends, FastAPI, HTTPException, Request

from server.db import doctor_appointments
from server.schema import (
    AppointmentModel,
    AppointmentModelOutput,
    DoctorModel,
    DoctorModelOutput,
    PatientModel,
    PatientModelOutput,
    SpecialityModel,
    SpecialityModelOutput,
)
from server.settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(dsn=settings.get_connection())
    yield
    await app.state.pool.close()


async def get_connection(request: Request):
    async with request.app.state.pool.acquire() as conn:
        yield conn


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/appointments", response_model=AppointmentModelOutput)
async def postapp(appointment: AppointmentModel, conn=Depends(get_connection)):
    start = appointment.start_time
    end = appointment.end_time

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="Время конца приёма должно быть после времени начала",
        )

    overlap = await doctor_appointments(conn, appointment)
    if overlap:
        raise HTTPException(
            status_code=409,
            detail="У доктора уже есть встреча в это время",
        )

    row = await conn.fetchrow(
        """
        INSERT INTO appointment (doctor_id, patient_id, start_time, end_time)
        VALUES ($1, $2, $3, $4)
        RETURNING id, doctor_id, patient_id, start_time, end_time;
        """,
        appointment.doctor_id,
        appointment.patient_id,
        start,
        end,
    )

    return AppointmentModelOutput(**row)


@app.get("/appointments/{meet_id}", response_model=AppointmentModelOutput)
async def getapp(meet_id: int, conn=Depends(get_connection)):
    row = await conn.fetchrow(
        """
        SELECT *
        FROM appointment
        WHERE id = $1
        """,
        meet_id,
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Указанной встречи не найдено",
        )

    appointment_dict = {
        "id": row[0],
        "doctor_id": row[1],
        "patient_id": row[2],
        "start_time": row[3],
        "end_time": row[4],
    }

    return AppointmentModelOutput(**appointment_dict)


@app.post("/patient", response_model=PatientModelOutput)
async def add_patient(patient: PatientModel, conn=Depends(get_connection)):
    row = await conn.fetchrow(
        """
        INSERT INTO patient (name, phone)
        VALUES ($1, $2)
        on conflict do nothing
        RETURNING id, name, phone;
        """,
        patient.name,
        patient.phone,
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с такими данными уже существует",
        )

    return PatientModelOutput(**row)


@app.post("/doctor", response_model=List[DoctorModelOutput])
async def add_doctor(doctor: DoctorModel, conn=Depends(get_connection)):
    row = await conn.fetchrow(
        """
        INSERT INTO doctor (full_name)
        VALUES ($1)
        on conflict do nothing
        RETURNING id, full_name;
        """,
        doctor.full_name,
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Доктор с такими данными уже существует",
        )

    return DoctorModelOutput(**row)


@app.post("/speciality", response_model=List[SpecialityModelOutput])
async def add_speciality(spec: SpecialityModel, conn=Depends(get_connection)):
    row = await conn.fetchrow(
        """
        INSERT INTO speciality (title)
        VALUES ($1)
        on conflict do nothing
        RETURNING id, title;
        """,
        spec.title,
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Специальность с таким названием уже существует",
        )

    return SpecialityModelOutput(**row)
