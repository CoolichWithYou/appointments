from sqlmodel import Session, select

from server.schema import Appointment


async def doctor_appointments(session: Session, appoint: Appointment) -> bool:
    statement = (
        select(Appointment)
        .where(Appointment.doctor_id == appoint.doctor_id)
        .where(Appointment.start_time <= appoint.end_time)
        .where(Appointment.end_time >= appoint.start_time)
    )
    overlap = session.exec(statement).first()

    if overlap:
        return True
    return False
