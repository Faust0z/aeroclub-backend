from ..extensions import db


class PaymentTypes(db.Model):
    __tablename__ = 'payment_types'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type: db.Mapped[str] = db.Column(db.String, nullable=False, unique=True)
    details: db.Mapped[str] = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"type=<{self.type} details={self.details}>"
