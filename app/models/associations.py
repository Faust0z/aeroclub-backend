from ..extensions import db
from sqlalchemy import ForeignKey

class ItineraryHasAirportCodes(db.Model):
    __tablename__ = 'itinerary_has_airport_codes'
    id_itinerarios_tienen_codigos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerarios_id = db.Column(db.Integer, ForeignKey('itineraries.id_itinerarios'))
    codigos_aeropuertos_id = db.Column(db.Integer, ForeignKey('airport_codes.id_codigos_aeropuertos'))

    itinerarios = db.relationship('Itineraries', back_populates='relaciones')
    codigosaeropuerto = db.relationship('AirportCodes', back_populates='relaciones')

class UsersHaveRoles(db.Model):
    __tablename__ = 'users_have_roles'
    id_usuarios_tiene_roles = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarios_id = db.Column(db.Integer, ForeignKey('users.id_usuarios'))
    roles_id = db.Column(db.Integer, ForeignKey('roles.id_roles'))

class UsersHaveInvoices(db.Model):
    __tablename__ = 'users_have_receipts'
    id_usuarios_tienen_recibos = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recibos_id = db.Column(db.Integer, db.ForeignKey('receipts.id_recibos'))
    usuarios_id = db.Column(db.Integer, db.ForeignKey('users.id_usuarios'))
    rol = db.Column(db.String(45), nullable=False,)

    usuarios = db.relationship('Users', back_populates='relaciones')
    recibos = db.relationship('Receipts', back_populates='relaciones')


""" 
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from ..extensions import db

# Itineraries ↔ AirportCodes
itinerary_has_airport_codes = Table(
    "itinerary_has_airport_codes",
    db.Model.metadata,
    Column("itinerarios_id", Integer, ForeignKey("itineraries.id_itinerarios"), primary_key=True),
    Column("codigos_aeropuertos_id", Integer, ForeignKey("airport_codes.id_codigos_aeropuertos"), primary_key=True),
)

# Users ↔ Roles
users_have_roles = Table(
    "users_have_roles",
    db.Model.metadata,
    Column("usuarios_id", Integer, ForeignKey("users.id_usuarios"), primary_key=True),
    Column("roles_id", Integer, ForeignKey("roles.id_roles"), primary_key=True),
)

# Users ↔ Receipts
users_have_invoices = Table(
    "users_have_invoices",
    db.Model.metadata,
    Column("usuarios_id", Integer, ForeignKey("users.id_usuarios"), primary_key=True),
    Column("recibos_id", Integer, ForeignKey("invoices.id_recibos"), primary_key=True),
    # ⚠️ If 'rol' is really needed, then this is not pure glue → should be a Model
    # Column("rol", String(45), nullable=False),
)
"""
