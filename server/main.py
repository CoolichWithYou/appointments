from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from server.db import engine
from server.interaction import doctor_appointments
from server.schema import (
    Appointment,
    AppointmentCreate,
    Doctor,
    DoctorCreate,
    Patient,
    PatientCreate,
    Speciality,
    SpecialityCreate,
)
from server.settings import Settings

settings = Settings()


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/appointment", response_model=Appointment)
async def postapp(
    appointment: AppointmentCreate,
    session: AsyncSession = Depends(get_session),
):
    appointment = Appointment.model_validate(appointment)

    start = appointment.start_time
    end = appointment.end_time

    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="Время конца приёма должно быть после времени начала",
        )

    overlap = await doctor_appointments(session, appointment)

    if overlap:
        raise HTTPException(
            status_code=409,
            detail="У доктора уже есть встреча в это время",
        )

    try:
        session.add(appointment)
        await session.commit()
        await session.refresh(appointment)
        return appointment
    except IntegrityError as e:
        await session.rollback()

        detail = str(e.orig)
        if "fk_doctor" in detail:
            raise HTTPException(
                status_code=404,
                detail="Доктор не найден",
            )
        elif "fk_patient" in detail:
            raise HTTPException(
                status_code=404,
                detail="Пациент не найден",
            )

        raise HTTPException(
            status_code=400,
            detail="Ошибка целостности данных",
        )


@app.get("/appointment/{meet_id}", response_model=Appointment)
async def getapp(
    meet_id: int,
    session: AsyncSession = Depends(get_session),
):
    appointment = session.get(Appointment, meet_id)

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Указанной встречи не найдено",
        )

    return appointment


@app.post("/patient", response_model=Patient)
async def add_patient(
    patient: PatientCreate,
    session: AsyncSession = Depends(get_session),
):
    stmt = (
        insert(Patient)
        .values(name=patient.name, phone=patient.phone)
        .on_conflict_do_nothing(
            index_elements=["phone"],
        )
        .returning(Patient.id, Patient.name, Patient.phone)
    )
    result = await session.exec(stmt)
    created = result.first()
    await session.commit()

    if not created:
        raise HTTPException(
            status_code=409,
            detail="Пациент с такими данными уже существует",
        )

    return created


@app.post("/doctor", response_model=Doctor)
async def add_doctor(
    doctor: DoctorCreate,
    session: AsyncSession = Depends(get_session),
):
    db_doctor = Doctor.model_validate(doctor)
    session.add(db_doctor)
    await session.commit()
    await session.refresh(db_doctor)
    return db_doctor


@app.post("/speciality", response_model=Speciality)
async def add_speciality(
    spec: SpecialityCreate, session: AsyncSession = Depends(get_session)
):
    stmt = (
        insert(Speciality)
        .values(title=spec.title)
        .on_conflict_do_nothing(
            index_elements=["title"],
        )
        .returning(Speciality.id, Speciality.title)
    )
    result = await session.exec(stmt)
    created = result.first()
    await session.commit()

    if not created:
        raise HTTPException(
            status_code=409,
            detail="Специальность с таким названием уже существует",
        )

    return created
