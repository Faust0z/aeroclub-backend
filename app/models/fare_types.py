from ..extensions import db


class PaymentTypes(db.Model):
    __tablename__ = 'payment_types'
    id_tipo_pago = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(45), nullable=False, unique=True)
    observaciones = db.Column(db.Text,nullable=True)
