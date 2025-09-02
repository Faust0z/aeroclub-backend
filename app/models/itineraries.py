from ..extensions import db
from sqlalchemy import ForeignKey


class Itineraries(db.Model):
    __tablename__ = 'itineraries'
    id_itinerarios = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hora_salida = db.Column(db.DateTime, nullable=False)
    hora_llegada = db.Column(db.DateTime, nullable=False)
    cantidad_aterrizajes = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String(255))
    tipo_itinerarios_id = db.Column(db.Integer, ForeignKey('itinerary_types.id_tipo_itinerarios'))
    aeronaves_id = db.Column(db.Integer, ForeignKey('planes.id_aeronaves'))
    RECIBOS_id_recibos = db.Column(db.Integer, ForeignKey('receipts.id_recibos'))

    # para borrar en cascada
    itinerariosRecibos = db.relationship('Receipts', back_populates='recibosItinerarios')


class AirportCodes(db.Model):
    __tablename__ = 'airport_codes'
    id_codigos_aeropuertos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_aeropuerto = db.Column(db.String(45))
