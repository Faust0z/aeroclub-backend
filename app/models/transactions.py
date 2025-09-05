from ..extensions import db
from datetime import date


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount: db.Mapped[float] = db.Column(db.Float, nullable=False)
    issued_date: db.Mapped[date] = db.Column(db.Date, nullable=False)
    description: db.Mapped[str] = db.Column(db.Text, nullable=True)
    fare_type_id = db.Column(db.ForeignKey('payment_types.id'))
    balance_id = db.Column(db.ForeignKey('balances.id'))

    def __repr__(self):
        return f"<Transaction amount={self.amount} issued_date={self.issued_date}>"
