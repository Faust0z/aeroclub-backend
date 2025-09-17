from ..extensions import db
from ..models import PaymentTypes


def get_payment_types_srv(type: str) -> PaymentTypes:
    return db.session.scalars(db.select(PaymentTypes).where(PaymentTypes.type == type)).all()
