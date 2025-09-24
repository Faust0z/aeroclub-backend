from sqlalchemy.exc import IntegrityError

from ..errors import AirportCodeAlreadyExists, AirportCodeNotFound
from ..extensions import db
from ..models import AirportCodes


def get_airport_codes_srv() -> list[AirportCodes]:
    return db.session.scalars(db.select(AirportCodes)).all()


def get_airport_code_by_code_srv(code: str) -> AirportCodes:
    airport_code = db.session.scalar_one_or_none(db.select(AirportCodes).where(AirportCodes.type == code))
    if not airport_code:
        raise AirportCodeNotFound
    return airport_code


def update_airport_code_srv(code: str, data: AirportCodes) -> AirportCodes:
    airport_code = get_airport_code_by_code_srv(code=code)
    try:
        for key, value in data.items():
            if hasattr(airport_code, key):
                setattr(airport_code, key, value)
        db.session.commit()
    except IntegrityError:
        raise AirportCodeAlreadyExists

    return airport_code
