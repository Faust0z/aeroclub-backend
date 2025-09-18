from sqlalchemy.exc import IntegrityError

from ..errors import PaymentTypeAlreadyExists
from ..extensions import db
from ..models import PaymentTypes


def get_payment_types_srv() -> list[PaymentTypes]:
    return db.session.scalars(db.select(PaymentTypes)).all()


def get_payment_type_by_name_srv(name: str) -> PaymentTypes:
    return db.session.scalar_one_or_none(db.select(PaymentTypes).where(PaymentTypes.type == name))


def update_payment_type_srv(name: str, data: PaymentTypes) -> PaymentTypes:
    payment_type = get_payment_type_by_name_srv(name=name)
    try:
        for key, value in data.items():
            if hasattr(payment_type, key):
                setattr(payment_type, key, value)
        db.session.commit()
    except IntegrityError:
        raise PaymentTypeAlreadyExists

    return payment_type
