from ..extensions import db


class ItineraryTypes(db.Model):
    __tablename__ = 'itinerary_types'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type: db.Mapped[str] = db.Column(db.String, unique=True)

    itinerary: db.Mapped[list["Itineraries"]] = db.relationship(back_populates="itinerary_types")

    def __repr__(self):
        return f"type=<{self.type}>"
