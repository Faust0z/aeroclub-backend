from ..extensions import db
from sqlalchemy import ForeignKey


class Balances(db.Model):
    __tablename__ = 'balances'
    id_cuenta_corriente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saldo_cuenta = db.Column(db.Float, nullable=False)
    usuarios_id = db.Column(db.Integer, ForeignKey('users.id_usuarios'), nullable=False)
