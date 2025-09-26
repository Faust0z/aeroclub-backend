from datetime import date

from ..extensions import db


class Fares(db.Model):
    __tablename__ = 'fares'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issued_date: db.Mapped[date] = db.Column(db.Date, nullable=False)
    fare_value: db.Mapped[float] = db.Column(db.Float, nullable=False)
    plane_id: db.Mapped[int] = db.Column(db.ForeignKey('planes.id'))

    plane: db.Mapped[list["Planes"]] = db.relationship(back_populates="fare")

    def __repr__(self):
        return f"<date_issued={self.issued_date} fare_value={self.fare_value}>"
