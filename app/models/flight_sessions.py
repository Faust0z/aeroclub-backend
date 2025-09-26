from datetime import date

from .associations import users_have_flight_sessions
from ..extensions import db


class FlightSessions(db.Model):
    __tablename__ = "flight_sessions"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_session_identifier: db.Mapped[int] = db.Column(db.Integer, nullable=False)
    issued_date: db.Mapped[date] = db.Column(db.Date, nullable=False)
    observations: db.Mapped[str] = db.Column(db.Text, nullable=True)
    transaction_id: db.Mapped[int] = db.Column(db.ForeignKey("transactions.id"))

    users: db.Mapped[list["Users"]] = db.relationship("Users", secondary=users_have_flight_sessions,
                                                      back_populates="flight_sessions")
    transactions: db.Mapped[list["Transactions"]] = db.relationship(back_populates="flight_sessions")
    itineraries: db.Mapped[list["Itineraries"]] = db.relationship(back_populates="flight_sessions")

    def __repr__(self):
        return f"<issued_date={self.issued_date} flight_session_identifier={self.flight_session_identifier}>"
