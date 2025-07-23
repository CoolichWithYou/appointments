from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from server.schema import Appointment


async def doctor_appointments(session: AsyncSession, appoint: Appointment) -> bool:
    statement = (
        select(Appointment)
        .where(Appointment.doctor_id == appoint.doctor_id)
        .where(Appointment.start_time <= appoint.end_time)
        .where(Appointment.end_time >= appoint.start_time)
    )
    result = await session.exec(statement)
    overlap = result.first()

    if overlap:
        return True
    return False
