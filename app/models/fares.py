from ..extensions import db
from datetime import date


class Fares(db.Model):
    __tablename__ = 'rates'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_issued: db.Mapped[date] = db.Column(db.Date, nullable=False)
    fare_value: db.Mapped[float] = db.Column(db.Float, nullable=False)
    instruction_cost: db.Mapped[float] = db.Column(db.Float, nullable=False)
    plane_id: db.Mapped[int] = db.Column(db.Integer, db.ForeignKey('planes.id'))

    def __repr__(self):
        return f"<date_issued={self.date_issued} fare_value={self.fare_value} instruction_cost={self.instruction_cost}>"
