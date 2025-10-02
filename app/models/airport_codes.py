from .associations import itinerary_has_airport_codes
from ..extensions import db


class AirportCodes(db.Model):
    __tablename__ = 'airport_codes'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code: db.Mapped[str] = db.Column(db.String(3), unique=True)

    itineraries: db.Mapped[list["Itineraries"]] = db.relationship("Itineraries", secondary=itinerary_has_airport_codes,
                                                                  back_populates="airport_codes")

    def __repr__(self):
        return f"<code={self.code}>"
