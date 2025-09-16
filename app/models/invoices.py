from datetime import date

from .associations import users_have_invoices
from ..extensions import db


class Invoices(db.Model):
    __tablename__ = "invoices"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issued_date: db.Mapped[date] = db.Column(db.Date, nullable=False)
    observations: db.Mapped[str] = db.Column(db.Text)
    transaction_id: db.Mapped[int] = db.Column(db.ForeignKey("transactions.id"))
    invoice_identifier: db.Mapped[int] = db.Column(db.Integer, nullable=False)

    user: db.Mapped[list["Users"]] = db.relationship("Users", secondary=users_have_invoices, back_populates="invoices")
    transaction: db.Mapped[list["Transactions"]] = db.relationship(back_populates="invoices")
    itinerary: db.Mapped[list["Itineraries"]] = db.relationship(back_populates="invoices")

    def __repr__(self):
        return f"<issued_date={self.issued_date} invoice_identifier={self.invoice_identifier}>"
