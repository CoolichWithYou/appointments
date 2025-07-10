from contextlib import asynccontextmanager

import asyncpg
from fastapi import Depends, FastAPI, HTTPException, Request

from server.db import doctor_appointments
from server.schema import AppointmentModel, AppointmentModelOutput
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
