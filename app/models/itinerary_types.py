from ..extensions import db


class ItineraryTypes(db.Model):
    __tablename__ = 'itinerary_types'
    id_tipo_itinerarios = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(45))
