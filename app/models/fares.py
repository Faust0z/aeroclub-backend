from ..extensions import db
from sqlalchemy import ForeignKey


class Fares(db.Model):
    __tablename__ = 'rates'
    id_tarifas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vigente_desde = db.Column(db.Date, nullable=False)
    importe_vuelo = db.Column(db.Float, nullable=False)
    importe_instruccion= db.Column(db.Float,nullable=False)
    aeronaves_id = db.Column(db.Integer, ForeignKey('planes.id_aeronaves'))
