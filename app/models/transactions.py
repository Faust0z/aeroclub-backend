from ..extensions import db
from sqlalchemy import ForeignKey


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id_transacciones = db.Column(db.Integer, primary_key=True, autoincrement=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.Text, nullable=True)
    tipo_pago_id = db.Column(db.Integer, ForeignKey('payment_types.id_tipo_pago'))
    cuenta_corriente_id = db.Column(db.Integer, ForeignKey('current_account.id_cuenta_corriente'))

    transaccionesRecibos = db.relationship('Receipts', back_populates='recibosTransacciones', cascade='all, delete-orphan')
