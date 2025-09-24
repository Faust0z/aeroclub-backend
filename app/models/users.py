from datetime import date

from app.models import FlightSessions
from .associations import users_have_roles, users_have_flight_sessions
from ..extensions import db


class Users(db.Model):
    __tablename__ = "users"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name: db.Mapped[str] = db.Column(db.String, nullable=False)
    last_name: db.Mapped[str] = db.Column(db.String, nullable=False)
    email: db.Mapped[str] = db.Column(db.String, nullable=False, unique=True)
    password: db.Mapped[str] = db.Column(db.String, nullable=False)
    phone_number: db.Mapped[str] = db.Column(db.String, nullable=False)
    created_at: db.Mapped[date] = db.Column(db.Date, nullable=False)
    disabled_at: db.Mapped[date] = db.Column(db.Date)
    address: db.Mapped[str] = db.Column(db.String)
    status: db.Mapped[bool] = db.Column(db.Boolean, nullable=False)

    balance: db.Mapped["Balances"] = db.relationship(back_populates="users")
    roles: db.Mapped[list["Roles"]] = db.relationship("Roles", secondary=users_have_roles, back_populates="users")
    flight_sessions: db.Mapped[list["FlightSessions"]] = db.relationship("FlightSessions",
                                                                         secondary=users_have_flight_sessions,
                                                                         back_populates="users")

    def __repr__(self):
        return f"<first_name={self.first_name} email={self.email}>"
