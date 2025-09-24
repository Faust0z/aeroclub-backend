from datetime import datetime

from .associations import itinerary_has_airport_codes
from ..extensions import db


class Itineraries(db.Model):
    __tablename__ = 'itineraries'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure_time: db.Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    arrival_time: db.Mapped[datetime] = db.Column(db.DateTime, nullable=False)
    landings_amount: db.Mapped[int] = db.Column(db.Integer, nullable=False)
    observations: db.Mapped[str] = db.Column(db.Text)
    itinerary_type_id: db.Mapped[int] = db.Column(db.ForeignKey('itinerary_types.id'))
    plane_id: db.Mapped[int] = db.Column(db.ForeignKey('planes.id'))
    invoice_id: db.Mapped[int] = db.Column(db.ForeignKey('invoices.id'))

    airport_codes: db.Mapped[list["AirportCodes"]] = db.relationship('AirportCodes', secondary=itinerary_has_airport_codes,
                                                                     back_populates="itineraries")
    invoice: db.Mapped["Invoices"] = db.relationship(back_populates="itineraries")
    itineary_type: db.Mapped["ItineraryTypes"] = db.relationship(back_populates="itineraries")
    plane: db.Mapped["Planes"] = db.relationship(back_populates="itineraries")

    def __repr__(self):
        return f"<departure_time={self.departure_time} arrival_time={self.arrival_time} landing_number={self.landings_amount}>"
