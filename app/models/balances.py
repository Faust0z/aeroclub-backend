from ..extensions import db


class Balances(db.Model):
    __tablename__ = 'balances'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    balance: db.Mapped[float] = db.Column(db.Float, nullable=False)
    user_id: db.Mapped[int] = db.Column(db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<balance={self.balance}>"
