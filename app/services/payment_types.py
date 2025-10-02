from sqlalchemy.exc import IntegrityError

from ..errors import PaymentTypeAlreadyExists, PaymentTypeNotFound
from ..extensions import db
from ..models import PaymentTypes


def get_payment_types_srv() -> list[PaymentTypes]:
    return db.session.scalars(db.select(PaymentTypes)).all()


def get_payment_type_by_name_srv(name: str) -> PaymentTypes:
    payment_type = db.session.execute(db.select(PaymentTypes).where(PaymentTypes.type == name)).scalar_one_or_none()
    if not payment_type:
        raise PaymentTypeNotFound
    return payment_type


def update_payment_type_srv(name: str, data: dict) -> PaymentTypes:
    payment_type = get_payment_type_by_name_srv(name=name)
    try:
        for key, value in data.items():
            if hasattr(payment_type, key):
                setattr(payment_type, key, value)
        db.session.commit()
    except IntegrityError:
        raise PaymentTypeAlreadyExists

    return payment_type
