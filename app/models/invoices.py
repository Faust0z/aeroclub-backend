from ..extensions import db
from datetime import date


class Invoices(db.Model):
    __tablename__ = "invoices"
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issued_date: db.Mapped[date] = db.Column(db.Date, nullable=False)
    observations: db.Mapped[str] = db.Column(db.Text)
    invoice_type_id: db.Mapped[int] = db.Column(db.ForeignKey("receipt_types.id"))
    transaction_id: db.Mapped[int] = db.Column(db.ForeignKey("transactions.id"))
    invoice_identifier: db.Mapped[int] = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<issued_date={self.issued_date} invoice_identifier={self.invoice_identifier}>"
