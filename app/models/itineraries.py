from ..extensions import db
from .associations import itinerary_has_airport_codes
from datetime import datetime


class Itineraries(db.Model):
    __tablename__ = 'itineraries'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure_time: db.Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    landing_time: db.Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    landings_amount: db.Mapped[int] = db.Column(db.Integer, nullable=False)
    observations: db.Mapped[str] = db.Column(db.Text)
    itinerary_type_id: db.Mapped[int] = db.Column(db.ForeignKey('itinerary_types.id'))
    plane_id: db.Mapped[int] = db.Column(db.ForeignKey('planes.id'))
    invoice_id: db.Mapped[int] = db.Column(db.ForeignKey('invoices.id'))

    airport_codes: db.Mapped[list["AirportCodes"]] = db.relationship('AirportCodes', secondary=itinerary_has_airport_codes,
                                                                     back_populates="itineraries")

    def __repr__(self):
        return f"<departure_time={self.departure_time} landing_time={self.landing_time} landing_number={self.landings_amount}>"
