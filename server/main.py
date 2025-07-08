from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
# TODO: psycopg to asyncpg
from psycopg_pool import AsyncConnectionPool

from schema import AppointmentModel
from settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=settings.get_db_connection())
    yield
    await app.async_pool.close()


app = FastAPI(lifespan=lifespan)


@app.post("/appointments")
async def get_appointments(request: Request, appointment: AppointmentModel) -> AppointmentModel:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO appointment (doctor_id, patient_id, start_time, end_time)
                    VALUES (%s,%s,%s,%s)
                    RETURNING id;
                """, [appointment.doctor_id, appointment.patient_id, appointment.start_time, appointment.end_time])
            results = await cur.fetchall()
            return results


@app.get("/appointments/{meet_id}")
async def say_hello(request: Request, meet_id: int) -> AppointmentModel | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT * FROM appointment WHERE id = %s
            """, [meet_id])
            result = await cur.fetchone()
            if result is None:
                return None

            appointment_dict = {
                "doctor_id": result[1],
                "patient_id": result[2],
                "start_time": result[3],
                "end_time": result[4]
            }

            return AppointmentModel(**appointment_dict)
